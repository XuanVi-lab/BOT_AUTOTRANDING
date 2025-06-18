from ssi_fc_data import fc_md_client, model
import config
import time
import os
from db_config import get_connection

client = fc_md_client.MarketDataClient(config)

def import_one_market(market):
    req = model.securities(market, 1, 1000)
    res = client.securities(config, req)
    data = res.get("data", [])

    print(f"\n📥 {market}: Tổng cộng {len(data)} dòng từ API")

    rows = []
    valid_symbols = []
    long_symbols = []
    skipped_symbols = []

    for item in data:
        symbol = item.get('Symbol')
        stock_name = item.get('StockName')
        stock_en = item.get('StockEnName')

        if isinstance(symbol, str):
            symbol = symbol.strip()
            if len(symbol) == 3 and isinstance(stock_name, str) and stock_name.strip():
                rows.append((
                    symbol,
                    stock_name.strip(),
                    market,
                    stock_en.strip() if isinstance(stock_en, str) else None
                ))
                valid_symbols.append(symbol)
            elif len(symbol) > 3:
                long_symbols.append(symbol)
            else:
                skipped_symbols.append(str(symbol))
        else:
            skipped_symbols.append(str(symbol))

    print(f"✅ {market}: {len(valid_symbols)} Symbol hợp lệ (3 ký tự)")
    print(f"🚫 {market}: {len(long_symbols)} Symbol bị loại (dài > 3 ký tự)")
    print(f"⚠️ {market}: {len(skipped_symbols)} Symbol không hợp lệ hoặc thiếu")

    # Ghi log ra file
    folder = r"e:\python\BOT_AUTOTRANDING\fc-data"
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, f"symbol_log_{market}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("✅ Symbol hợp lệ (3 ký tự):\n")
        for s in valid_symbols:
            f.write(f"{s}\n")
        f.write("\n🚫 Symbol dài > 3:\n")
        for s in long_symbols:
            f.write(f"{s}\n")
        f.write("\n⚠️ Symbol không hợp lệ hoặc thiếu:\n")
        for s in skipped_symbols:
            f.write(f"{s}\n")

    print(f"📝 Đã ghi log ra file: {filename}")

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

# Gọi lần lượt từng sàn
for market in ['HOSE', 'HNX', 'UPCOM']:
    import_one_market(market)
    time.sleep(1.2)
