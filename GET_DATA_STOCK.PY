import requests
import pandas as pd
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_price_ssi(symbol, start_date, end_date):
    """
    Lấy dữ liệu giá cổ phiếu từ API SSI (https://iboard-api.ssi.com.vn)
    """
    start_ts = int(pd.Timestamp(start_date).timestamp())
    end_ts = int(pd.Timestamp(end_date).timestamp())

    url = f"https://iboard-api.ssi.com.vn/statistics/charts/history?resolution=1D&symbol={symbol}&from={start_ts}&to={end_ts}"
    print(f"\n📥 Đang lấy dữ liệu: {symbol}")
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10, verify=False)
        print(f"📨 Trạng thái HTTP: {r.status_code}")

        # Parse JSON và lấy phần 'data'
        json_data = r.json()
        data = json_data.get("data", {})

        if not data or 't' not in data:
            print(f"⚠️ Không có dữ liệu hợp lệ cho {symbol}")
            print("📨 Phản hồi ngắn:", r.text[:200])
            return None

        df = pd.DataFrame({
            'Date': pd.to_datetime(data['t'], unit='s'),
            'Open': data['o'],
            'High': data['h'],
            'Low': data['l'],
            'Close': data['c'],
            'Volume': data['v'],
        })
        df['Symbol'] = symbol
        return df

    except Exception as e:
        print(f"❌ Lỗi kết nối với {symbol}: {e}")
        return None


def get_all_stocks(symbols, start_date, end_date, save_file='all_stocks_data.csv'):
    """
    Lấy dữ liệu cho danh sách mã và lưu file CSV
    """
    all_data = []

    for sym in symbols:
        df = get_price_ssi(sym, start_date, end_date)
        if df is not None:
            all_data.append(df)

    if all_data:
        result = pd.concat(all_data, ignore_index=True)
        result.to_csv(save_file, index=False)
        print(f"\n✅ Đã lưu dữ liệu vào: {save_file}")
    else:
        print("\n⚠️ Không có dữ liệu nào được lưu.")


# ==============================
# 👉 Sử dụng:

if __name__ == "__main__":
    stock_list = ["HPG", "HAG"]
    save_path = "E://python//BOT_AUTOTRANDING//all_stocks_data.csv"
    get_all_stocks(stock_list, start_date="2010-01-01", end_date="2024-06-30", save_file=save_path)
