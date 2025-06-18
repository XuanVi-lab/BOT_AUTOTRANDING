from ssi_fc_data import fc_md_client, model
import pandas as pd
import time
import os
import config  # Đảm bảo đã có file config.py trong thư mục

# Xoá màn hình nếu đang chạy trong terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Khởi tạo client
client = fc_md_client.MarketDataClient(config)

# Hàm lấy dữ liệu một sàn
def get_market_data(market):
    req = model.securities(market, 1, 1000)
    res = client.securities(config, req)
    data = res.get("data", [])

    rows = []

    for item in data:
        symbol = (item.get('Symbol') or '').strip()
        stock_name = (item.get('StockName') or '').strip()
        stock_en = (item.get('StockEnName') or '').strip()
        industry = (item.get('IndustryName') or '').strip()

        if symbol and len(symbol) == 3 and stock_name:
            rows.append({
                'symbol': symbol,
                'name_vn': stock_name,
                'name_en': stock_en,
                'industry': industry,
                'exchange': market
            })

    return rows

# Lấy và kết hợp dữ liệu từ 3 sàn
all_data = []
for market in ['HOSE', 'HNX', 'UPCOM']:
    all_data.extend(get_market_data(market))
    time.sleep(1)  # Tránh gửi request quá nhanh

# Tạo DataFrame và lưu ra Excel
df = pd.DataFrame(all_data)
df.to_excel("d:\\DanhSach_CoPhieu_SSI.xlsx", index=False)
print("📁 Đã lưu file: DanhSach_CoPhieu_SSI.xlsx")


# import ssi_fc_data.fc_md_client as fc
# print(fc.__file__)