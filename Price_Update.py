import requests
import pandas as pd
import time
import urllib3
from db_config import get_connection
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_price_ssi(symbol, start_date, end_date):
    start_ts = int(pd.Timestamp(start_date).timestamp())
    end_ts = int(pd.Timestamp(end_date).timestamp())

    url = f"https://iboard-api.ssi.com.vn/statistics/charts/history?resolution=1D&symbol={symbol}&from={start_ts}&to={end_ts}"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}

    try:
        r = requests.get(url, headers=headers, timeout=10, verify=False)
        json_data = r.json()
        data = json_data.get("data", {})

        if not data or 't' not in data or not data['t']:
            print(f"⚠️ Không có dữ liệu cho: {symbol}")
            return None

        df = pd.DataFrame({
            'symbol': symbol,
            'trade_date': pd.to_datetime(data['t'], unit='s'),
            'open': data['o'],
            'high': data['h'],
            'low': data['l'],
            'close': data['c'],
            'volume': data['v'],
        })
        return df

    except Exception as e:
        print(f"❌ Lỗi lấy dữ liệu {symbol}: {e}")
        return None

def insert_price_data(df, conn):
    cursor = conn.cursor()
    for _, row in df.iterrows():
        try:
            cursor.execute("""
                IF NOT EXISTS (
                    SELECT 1 FROM price_data
                    WHERE [symbol] = ? AND [trade_date] = ?
                )
                INSERT INTO price_data ([symbol], [trade_date], [open], [high], [low], [close], [volume])
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, row.symbol, row.trade_date, row.symbol, row.trade_date,
                row.open, row.high, row.low, row.close, row.volume)

        except Exception as e:
            print(f"❌ DB lỗi {row.symbol} {row.trade_date}: {e}")
    conn.commit()

def get_all_symbols():
    conn = get_connection()
    df = pd.read_sql("select [stock_list].[symbol] from stock_list where [stock_list].[symbol] not in (SELECT  b.[symbol]  FROM [BOT_AUTOTRADING].[dbo].[price_data] AS b)", conn)
    conn.close()
    return df['symbol'].tolist()

def update_all_stock_prices(start_date="2005-01-01", end_date="2024-06-30"):
    symbols = get_all_symbols()
    conn = get_connection()

    for symbol in symbols:
        print(f"\n📊 Đang xử lý: {symbol}")
        df = get_price_ssi(symbol, start_date, end_date)
        if df is not None and not df.empty:
            insert_price_data(df, conn)
        else:
            print(f"⏭️ Bỏ qua: {symbol} – không có dữ liệu.")
        time.sleep(0.5)

    conn.close()
    print("\n✅ Hoàn tất cập nhật dữ liệu lịch sử.")

if __name__ == "__main__":
    update_all_stock_prices()
