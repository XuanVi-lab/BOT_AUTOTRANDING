import requests
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_sector_stocks(stock_list):
    url = "https://iboard-query.ssi.com.vn/stock/multiple"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "stocks": stock_list
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10, verify=False)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            print(f"✅ Lấy thành công {len(df)} cổ phiếu.")
            return df
        else:
            print(f"❌ Lỗi: HTTP {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Lỗi kết nối HTTPS: {e}")
        return None


if __name__ == "__main__":
    dau_khi_stocks = ["PVC", "PVE", "PVB", "TOS", "POS", "PVS", "PVD", "BSR", "PEQ", "PLX", "OIL", "PTV"]
    df = fetch_sector_stocks(dau_khi_stocks)

    if df is not None:
        df.to_csv("E://python//BOT_AUTOTRANDING//dau_khi_stocks.csv", index=False, encoding="utf-8-sig")
        print("📁 Đã lưu file: dau_khi_stocks.csv")
