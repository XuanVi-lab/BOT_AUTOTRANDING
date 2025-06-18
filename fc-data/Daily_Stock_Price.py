from ssi_fc_data import fc_md_client, model
import config
import json

# Khởi tạo client
client = fc_md_client.MarketDataClient(config)

# Gọi dữ liệu giá cổ phiếu
result = client.daily_stock_price(
    config,
    model.daily_stock_price('HAG', '12/06/2025', '12/06/2025', 1, 100, 'hose')
)

# Xuất ra file JSON
with open("e:\\python\\BOT_AUTOTRANDING\\fc-data\\daily_stock_HAG.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("✅ Đã ghi file JSON: daily_stock_HAG.json")
