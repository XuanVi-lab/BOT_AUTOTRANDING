import requests
import pyodbc
import time
from db_config import get_connection  # Bạn đã có sẵn

# Khai báo cấu hình SSI FastConnect API
CONSUMER_ID = "your_consumer_id"
CONSUMER_SECRET = "your_consumer_secret"
ACCESS_TOKEN = "your_access_token"

BASE_URL = "https://api-iboard.ssi.com.vn/fc"

HEADERS = {
    "consumerId": CONSUMER_ID,
    "consumerSecret": CONSUMER_SECRET,
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

def fetch_stock_info(symbol):
    url = f"{BASE_URL}/stock/overview/basic-info?code={symbol}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ {symbol} - HTTP {response.status_code}")
        return None

def update_database(symbol, info):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE stock_list
            SET 
                listed_shares = ?,
                outstanding_shares = ?,
                charter_capital = ?,
                listed_date = ?,
                par_value = ?,
                floor_price = ?
            WHERE symbol = ?
        """, (
            info.get("listedShares"),
            info.get("outstandingShares"),
            info.get("charterCapital"),
            info.get("listedDate"),
            info.get("parValue"),
            info.get("floorPrice"),
            symbol
        ))
        conn.commit()
    except Exception as e:
        print(f"⚠️ Lỗi cập nhật {symbol}: {e}")
    finally:
        conn.close()

def run():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT symbol FROM stock_list")
    symbols = [row[0] for row in cursor.fetchall()]
    conn.close()

    print(f"🚀 Bắt đầu cập nhật {len(symbols)} cổ phiếu...")
    for i, symbol in enumerate(symbols, start=1):
        info = fetch_stock_info(symbol)
        if info:
            update_database(symbol, info)
        time.sleep(0.3)  # để tránh bị giới hạn request
        print(f"✅ {i}/{len(symbols)}: {symbol} xong")

if __name__ == "__main__":
    run()
