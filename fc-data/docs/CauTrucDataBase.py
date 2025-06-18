import pandas as pd
from datetime import datetime
import os

# Define table schemas as a list of dictionaries
tables = {
    "stock_list": [
        ["symbol", "NVARCHAR(20)", "Mã cổ phiếu (khóa chính)"],
        ["StockName", "NVARCHAR(255)", "Tên công ty niêm yết"],
        ["StockEnName", "NVARCHAR(255)", "Tên công ty (tiếng Anh)"],
        ["industry_code", "VARCHAR(20)", "Mã ngành (liên kết bảng industry)"],
        ["Market", "VARCHAR(10)", "Sàn niêm yết (HOSE, HNX, UPCOM)"],
        ["listed_shares", "BIGINT", "KL cổ phiếu đang niêm yết"],
        ["outstanding_shares", "BIGINT", "KL cổ phiếu đang lưu hành"],
        ["capital", "BIGINT", "Vốn điều lệ"],
        ["par_value", "FLOAT", "Mệnh giá niêm yết"],
        ["listed_date", "DATE", "Ngày niêm yết"],
        ["ipo_price", "FLOAT", "Giá IPO ban đầu"],
        ["status", "VARCHAR(50)", "Trạng thái (HOẠT ĐỘNG, HỦY NIÊM YẾT, v.v.)"],
        ["sector", "NVARCHAR(255)", "Ngành chính phân tích"],
        ["sub_sector", "NVARCHAR(255)", "Ngành phụ nếu có"],
        ["last_updated", "DATETIME", "Ngày cập nhật cuối cùng dữ liệu từ SSI"],
    ],
    "industry": [
        ["industry_code", "VARCHAR(20)", "Mã ngành (khóa chính)"],
        ["industry_name", "NVARCHAR(255)", "Tên ngành"],
    ],
    "price_data": [
        ["symbol", "NVARCHAR(20)", "Mã cổ phiếu"],
        ["trade_date", "DATE", "Ngày giao dịch"],
        ["open", "FLOAT", "Giá mở cửa"],
        ["high", "FLOAT", "Giá cao nhất"],
        ["low", "FLOAT", "Giá thấp nhất"],
        ["close", "FLOAT", "Giá đóng cửa"],
        ["volume", "BIGINT", "Khối lượng giao dịch"],
    ],
    "index_data": [
        ["index_code", "VARCHAR(20)", "Mã chỉ số"],
        ["trade_date", "DATE", "Ngày giao dịch"],
        ["open", "FLOAT", "Giá mở"],
        ["high", "FLOAT", "Giá cao nhất"],
        ["low", "FLOAT", "Giá thấp nhất"],
        ["close", "FLOAT", "Giá đóng cửa"],
        ["volume", "BIGINT", "Tổng KL cổ phiếu trong chỉ số"],
    ],
    "signals": [
        ["symbol", "NVARCHAR(20)", "Mã cổ phiếu"],
        ["trade_date", "DATE", "Ngày phát hiện tín hiệu"],
        ["signal_type", "VARCHAR(50)", "Loại tín hiệu (BUY, SELL, CROSS, v.v.)"],
        ["description", "TEXT", "Mô tả tín hiệu nếu cần"],
    ],
    "trades": [
        ["trade_id", "INT (PK)", "ID giao dịch (tự tăng)"],
        ["symbol", "NVARCHAR(20)", "Mã cổ phiếu"],
        ["trade_date", "DATE", "Ngày khởi tạo tín hiệu giao dịch"],
        ["action", "VARCHAR(10)", "Hành động (BUY / SELL)"],
        ["quantity", "INT", "KL mua hoặc bán"],
        ["entry_price", "FLOAT", "Giá mua vào"],
        ["exit_price", "FLOAT", "Giá bán ra"],
        ["exit_date", "DATE", "Ngày bán ra"],
        ["pnl", "FLOAT", "Lợi nhuận (PnL = exit - entry)"],
        ["strategy", "VARCHAR(50)", "Chiến lược áp dụng (e.g. MACD, Ichimoku)"],
        ["success", "BIT", "Thành công (1: có lời, 0: lỗ)"],
    ]
}

# Save to Excel
excel_path = "/mnt/data/Stock_Database_Schema.xlsx"
with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
    for table_name, schema in tables.items():
        df = pd.DataFrame(schema, columns=["Cột", "Kiểu dữ liệu", "Ý nghĩa"])
        df.to_excel(writer, sheet_name=table_name, index=False)

excel_path