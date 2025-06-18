import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import pyodbc
from datetime import datetime
from ssi_fc_data import fc_md_client, model
import config
from db_config import get_connection

client = fc_md_client.MarketDataClient(config)

def fetch_stock_details(symbol):
    try:
        req = model.securities_details('HOSE', symbol, 1, 1)
        result = client.securities_details(config, req)
        if result["status"] == 200 and result["data"]:
            return result["data"][0]
    except Exception as e:
        print(f"❌ API lỗi với {symbol}: {e}")
    return None

def update_stock_list():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT symbol FROM stock_list WHERE LEN(symbol) <= 3")
    symbols = [row.symbol for row in cursor.fetchall()]

    for symbol in symbols:
        data = fetch_stock_details(symbol)
        if not data:
            continue

        try:
            cursor.execute("""
                UPDATE stock_list SET
                    name = ?,
                    exchange = ?,
                    listed_shares = ?,
                    outstanding_shares = ?,
                    par_value = ?,
                    listed_date = ?,
                    ipo_price = ?,
                    capital = ?,
                    status = ?,
                    last_updated = GETDATE()
                WHERE symbol = ?
            """,
            data.get("stockName"),
            data.get("market"),
            data.get("listedShareCount"),
            data.get("outstandingShare"),
            data.get("parValue"),
            data.get("listedDate"),
            data.get("ipoPrice"),
            data.get("charterCapital"),
            data.get("status"),
            symbol)

            print(f"✅ Cập nhật {symbol} thành công.")
        except Exception as e:
            print(f"❌ Lỗi cập nhật {symbol}: {e}")

    conn.commit()
    conn.close()
    print("\n✅ Hoàn tất cập nhật thông tin cổ phiếu.")

if __name__ == "__main__":
    update_stock_list()
