

from vnstock import Company, Listing
import ssi_fc_data.fc_md_client as fc
import warnings
from ssi_fc_data import fc_md_client, model
import pandas as pd
import time
import os
import config  # Đảm bảo đã có file config.py trong thư mục
print("⚙️ Loại config:", type(config))


warnings.filterwarnings("ignore", category=FutureWarning)

print(fc.__file__)
# Xoá màn hình nếu đang chạy trong terminal
os.system('cls' if os.name == 'nt' else 'clear')


# --- PHẦN 1: LẤY DỮ LIỆU TỪ SSI (Đã có sẵn file, không cần chạy lại nếu đã tạo) ---
# Khởi tạo client
client = fc_md_client.MarketDataClient(config)

# Hàm lấy dữ liệu một sàn


def get_market_data(market):
    req = model.securities(market, 1, 1000)
    res = client.securities(config, req)
    data = res.get("data", [])

    print(f"📦 Số lượng item trả về từ {market}: {len(data)}")
    if data:
        sample = data[0]
        # print(f"🔍 Số lượng trường trong mỗi item: {len(sample)}")
        print(f"📋 Danh sách trường: {list(sample.keys())}")
    else:
        print("⚠️ Không có dữ liệu trong phản hồi.")
    # for item in data[:5]:  # in thử vài dòng đầu
    #     print(item)

    rows = []

    for item in data:
        symbol = (item.get('Symbol') or '').strip()
        stock_name = (item.get('StockName') or '').strip()
        stock_en = (item.get('StockEnName') or '').strip()
        # industry = (item.get('IndustryName') or '').strip()

        if symbol and len(symbol) == 3 and stock_name:
            rows.append({
                'symbol': symbol,
                'name_vn': stock_name,
                'name_en': stock_en,
                # 'industry': industry,
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


# --- PHẦN 2: ĐỌC FILE + LẤY DỮ LIỆU vnstock ---

# warnings.filterwarnings("ignore", category=FutureWarning)
# os.environ['REQUESTS_CA_BUNDLE'] = r'e:\python\certs\certificate_chain_vietcap.pem'
# # Lấy danh sách mã + sàn + tên công ty
# listing = Listing()
# df_exchange = listing.symbols_by_exchange()
# df_names = listing.symbols_by_industries()[['symbol', 'organ_name']]

# # Lấy 5 mã đầu
# symbols = df_exchange['symbol'].tolist()[:5]

# results = []
# for symbol in symbols:
#     try:
#         company = Company(symbol=symbol, source='VCI')
#         info = company.overview()
#         results.append(info)
#         print(f"✅ {symbol} OK")
#         time.sleep(1.5)
#     except Exception as e:
#         print(f"❌ {symbol} lỗi: {e}")

# # Gộp dữ liệu
# df_info = pd.concat(results, ignore_index=True)
# df_merge = pd.merge(df_info, df_exchange[['symbol', 'exchange']], on='symbol', how='left')
# df_merge = pd.merge(df_merge, df_names, on='symbol', how='left')  # ghép thêm tên công ty

# # Đổi tên cột và sắp xếp
# df_final = df_merge[[
#     'symbol', 'id', 'issue_share', 'history',
#     'organ_name',  # tên công ty tiếng Việt
#     'icb_name3', 'icb_name2', 'icb_name4',
#     'financial_ratio_issue_share', 'charter_capital', 'exchange'
# ]].rename(columns={
#     'symbol': 'Mã cổ phiếu',
#     'organ_name': 'Tên công ty (VN)',
#     'icb_name3': 'Ngành cấp 3',
#     'icb_name2': 'Ngành cấp 2',
#     'icb_name4': 'Ngành chi tiết',
#     'financial_ratio_issue_share': 'Số CP phân tích',
#     'charter_capital': 'Vốn điều lệ',
#     'exchange': 'Sàn giao dịch'
# })

# # Xuất file
# df_final.to_excel("d:\\ThongTin_5Ma_CO_TEN_CONG_TY.xlsx", index=False)
# print("📁 Đã lưu file: ThongTin_5Ma_CO_TEN_CONG_TY.xlsx")
# Tắt cảnh báo không quan trọng
warnings.filterwarnings("ignore", category=FutureWarning)

# Chỉ định chứng chỉ SSL nếu cần
os.environ['REQUESTS_CA_BUNDLE'] = r'e:\python\certs\certificate_chain_vietcap.pem'

# Đọc danh sách mã cổ phiếu từ file Excel (đã lấy từ SSI ở phần 1)


# df_input = pd.read_excel("d:\\DanhSach_CoPhieu_SSI.xlsx")

# # Lọc các cột cần thiết: symbol, exchange, name_vn

# df_input = df_input[['symbol', 'exchange', 'name_vn']].dropna()
# symbols = df_input['symbol'].tolist()[:5]  # Lấy 5 mã đầu để test

df_ssi = pd.read_excel("d:\\DanhSach_CoPhieu_SSI.xlsx")
results = []

# for symbol in symbols:
for symbol in df_ssi['symbol'].tolist()[:50]:
    # for symbol in df_ssi['symbol'].tolist():
    try:
        company = Company(symbol=symbol, source='VCI')
        info = company.overview()
        results.append(info)
        print(f"✅ {symbol} OK")
        time.sleep(1.2)
    except Exception as e:
        print(f"❌ {symbol} lỗi: {e}")

if results:
    df_vnstock = pd.concat(results, ignore_index=True)

    # Gộp dữ liệu
    df_merged = pd.merge(df_ssi, df_vnstock, on='symbol', how='right')

    # Đổi tên và chọn cột
    df_final = df_merged[[
        'symbol', 'name_vn', 'name_en',  'exchange',
        'icb_name2', 'icb_name3', 'icb_name4',
        'issue_share', 'charter_capital', 'financial_ratio_issue_share'
    ]].rename(columns={
        'symbol': 'symbol',
        'name_vn': 'StockName',
        'name_en': 'StockEnName',
        # 'industry': 'Ngành',
        'exchange': 'Market',
        'icb_name2': 'NganhCap2',
        'icb_name3': 'NganhCap3',
        'icb_name4': 'NganhChiTiet',
        'issue_share': 'SoCPNiemYet',
        'charter_capital': 'VonDieuLe',
        'financial_ratio_issue_share': 'SoCPPhanTich'
    })
    # print(df_final.head(10))
    # Xuất file kết quả
    df_final.to_excel("d:\\ThongTin_Du_ThongTin.xlsx", index=False)
    print("📁 Đã lưu file: ThongTin_Du_ThongTin.xlsx")
else:
    print("⚠️ Không có mã nào trả về dữ liệu hợp lệ.")
