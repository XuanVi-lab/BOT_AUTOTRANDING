from ssi_fc_data import fc_md_client, model
import config
import time
from db_config import get_connection

client = fc_md_client.MarketDataClient(config)

def import_one_market(market):
    req = model.securities(market, 1, 1000)
    res = client.securities(config, req)
    data = res.get("data", [])

    print(f"\n📥 {market}: Tổng cộng {len(data)} dòng từ API")

    rows = []
    count_valid = 0
    count_invalid = 0

    for item in data:
        symbol = item.get('Symbol')
        stock_name = item.get('StockName')
        stock_en = item.get('StockEnName')

        if isinstance(symbol, str):
            symbol = symbol.strip()
            if len(symbol) == 3 and not symbol.upper().startswith("C") and isinstance(stock_name, str) and stock_name.strip():
                rows.append((
                    symbol,
                    stock_name.strip(),
                    market,
                    stock_en.strip() if isinstance(stock_en, str) else None
                ))
                count_valid += 1
            elif len(symbol) > 3:
                count_invalid += 1

    print(f"✅ {market}: {count_valid} Symbol hợp lệ (3 ký tự)")
    print(f"🚫 {market}: {count_invalid} Symbol bị loại (dài > 3 ký tự)")

    for i, row in enumerate(rows[:5]):
        print(f"➡️ Dòng {i+1}: {row}")

    if not rows:
        print(f"⚠️ Không có dữ liệu hợp lệ cho {market}")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO [dbo].[CODE_STOCK] ([symbol], [StockName], [Market], [StockEnName])
        VALUES (?, ?, ?, ?)
        """
        cursor.executemany(insert_query, rows)
        conn.commit()
        print(f"✅ Đã import thành công {len(rows)} dòng cho {market}")
    except Exception as e:
        print(f"❌ Lỗi khi import {market}: {e}")
    finally:
        conn.close()

# Chạy lần lượt từng sàn
for market in ['HOSE', 'HNX', 'UPCOM']:
    import_one_market(market)
    time.sleep(1.2)
