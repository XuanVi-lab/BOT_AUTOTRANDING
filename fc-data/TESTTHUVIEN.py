import os
import pandas as pd
import time
from ssi_fc_data import fc_md_client, model
import config
from vnstock import Company
# # Xóa màn hình
os.system('cls' if os.name == 'nt' else 'clear')
# Bỏ xác minh SSL nếu cần
# os.environ['CURL_CA_BUNDLE'] = ''
# os.environ['PYTHONHTTPSVERIFY'] = '0'

# --- PHẦN 1: LẤY DỮ LIỆU TỪ SSI (Đã có sẵn file, không cần chạy lại nếu đã tạo) ---
# Nếu chưa có file d:\\DanhSach_CoPhieu_SSI.xlsx thì chạy phần này
# Khởi tạo client SSI
client = fc_md_client.MarketDataClient(config)

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

# Lấy và lưu file nếu cần
all_data = []
for market in ['HOSE', 'HNX', 'UPCOM']:
    all_data.extend(get_market_data(market))
    time.sleep(1)

df_ssi = pd.DataFrame(all_data)
df_ssi.to_excel("d:\\DanhSach_CoPhieu_SSI.xlsx", index=False)
print("✅ Đã lưu: DanhSach_CoPhieu_SSI.xlsx")





# --- PHẦN 2: ĐỌC FILE + LẤY DỮ LIỆU vnstock ---
df_ssi = pd.read_excel("d:\\DanhSach_CoPhieu_SSI.xlsx")

results = []
for symbol in df_ssi['symbol'].tolist():
    try:
        company = Company(symbol=symbol, source='VCI')
        info = company.overview()
        results.append(info)
        print(f"✅ {symbol} OK")
        time.sleep(1.2)
    except Exception as e:
        print(f"❌ {symbol} lỗi: {e}")

df_vnstock = pd.concat(results, ignore_index=True)

# Gộp dữ liệu
df_merged = pd.merge(df_ssi, df_vnstock, on='symbol', how='left')

# Đổi tên và chọn cột
df_final = df_merged[[ 
    'symbol', 'name_vn', 'name_en', 'industry', 'exchange',
    'icb_name2', 'icb_name3', 'icb_name4',
    'issue_share', 'charter_capital', 'financial_ratio_issue_share'
]].rename(columns={
    'symbol': 'Mã cổ phiếu',
    'name_vn': 'Tên công ty (VN)',
    'name_en': 'Tên công ty (EN)',
    'industry': 'Ngành',
    'exchange': 'Sàn giao dịch',
    'icb_name2': 'Ngành cấp 2',
    'icb_name3': 'Ngành cấp 3',
    'icb_name4': 'Ngành chi tiết',
    'issue_share': 'Số CP niêm yết',
    'charter_capital': 'Vốn điều lệ',
    'financial_ratio_issue_share': 'Số CP phân tích'
})

# Xuất file kết quả
df_final.to_excel("d:\\ThongTin_Du_ThongTin.xlsx", index=False)
print("📁 Đã lưu file: ThongTin_Du_ThongTin.xlsx")
