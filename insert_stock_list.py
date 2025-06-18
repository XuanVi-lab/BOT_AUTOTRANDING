import json
from db_config import get_connection  # Đảm bảo file db_config.py có hàm này

def insert_stocks_by_industry(input_file):
    conn = get_connection()
    cursor = conn.cursor()

    with open(input_file, "r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue
            try:
                data = json.loads(line.strip())
                industry_code = next(k for k in data if k != "stocks")
                stocks = data["stocks"]

                for stock in stocks:
                    if len(stock.strip()) > 3:
                        continue  # 👉 Bỏ qua mã cổ phiếu > 3 ký tự
                    cursor.execute("""
                        IF NOT EXISTS (
                            SELECT 1 FROM stock_list WHERE symbol = ? AND industry_code = ?
                        )
                        BEGIN
                            INSERT INTO stock_list (symbol, industry_code)
                            VALUES (?, ?)
                        END
                    """, stock, industry_code, stock, industry_code)

            except Exception as e:
                print(f"❌ Lỗi dòng: {line.strip()[:100]}... | Chi tiết: {e}")

    conn.commit()
    conn.close()
    print("✅ Hoàn tất chèn dữ liệu cổ phiếu theo ngành.")

# === Gọi hàm chính ===
if __name__ == "__main__":
    insert_stocks_by_industry("E:\\python\\BOT_AUTOTRANDING\\CK_TheoNganh.txt")
