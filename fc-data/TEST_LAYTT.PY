
import os
from ssi_fc_data import fc_md_client, model
import config
# -----------
# Xóa màn hình
os.system('cls' if os.name == 'nt' else 'clear')
client = fc_md_client.MarketDataClient(config)

# print(client.daily_stock_price(config, model.daily_stock_price ('HAG', '12/06/2025', '12/06/2025', 1, 100, 'hose')))
# req = model.securities('VN30', 1, 100)
# response = client.securities(config, req)
# print(F"SAN HOSE :\n {response}")


# print(client.index_components(config, model.index_components('vn30', 1, 100)))
# print(client.daily_index(config, model.daily_index( '123', 'VNINDEX', '11/06/2025', '11/06/2025', 1, 100, '', '')))


# print(client.daily_ohlc(config, model.daily_ohlc('HAG', '12/06/2025', '12/06/2025', 1, 100, True)))
# print(client.intraday_ohlc(config, model.intraday_ohlc('HAG', '12/06/2025', '12/06/2025', 1, 100, True, 1)))
# print(client.securities_details(config, model.securities_details('HOSE', 'HAG', 1, 100)))    


print(client.daily_stock_price(config, model.daily_stock_price ('HAG', '12/06/2025', '12/06/2025', 1, 100, 'HOSE')))

# print(client.daily_ohlc(config, model.daily_ohlc('ssi', '11/06/2025', '11/06/2025', 1, 120, True)))
# model.daily_ohlc('SSI', '01/01/2010', '11/06/2025', pageIndex=2, pageSize=100, ascending=True)

# # # -----------
# req = model.securities('HNX', 1, 100)
# response = client.securities(config, req)
# print(F"SAN HNX :\n {response}")

# # # -----------
# req = model.securities('UPCOM', 1, 100)
# response = client.securities(config, req)
# print(F"SAN UPCOM :\n {response}")


'''
from ssi_fc_data import fc_md_client, model
import config

client = fc_md_client.MarketDataClient(config)

def fetch_all_ohlc(symbol, start_date, end_date, page_size=100):
    all_data = []
    page_index = 1
    ascending = True

    while True:
        req = model.daily_ohlc(symbol, start_date, end_date, page_index, page_size, ascending)
        response = client.daily_ohlc(config, req)

        if response['data']:
            all_data.extend(response['data'])
            page_index += 1
        else:
            break

    return all_data

# Gọi hàm
symbol = 'SSI'
start_date = '01/01/2010'
end_date = '11/06/2025'
ohlc_data = fetch_all_ohlc(symbol, start_date, end_date)

print(f"Tổng số bản ghi thu được: {len(ohlc_data)}")


'''