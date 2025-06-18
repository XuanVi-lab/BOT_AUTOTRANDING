-- ⚙️ Ràng buộc: stock_list ↔ industry
ALTER TABLE stock_list
ADD CONSTRAINT FK_stocklist_industry
FOREIGN KEY (industry_code)
REFERENCES industry(industry_code);

-- ⚙️ Ràng buộc: price_data ↔ stock_list
ALTER TABLE price_data
ADD CONSTRAINT FK_pricedata_stock
FOREIGN KEY (symbol)
REFERENCES stock_list(symbol);

-- ⚙️ Ràng buộc: signals ↔ stock_list
ALTER TABLE signals
ADD CONSTRAINT FK_signals_stock
FOREIGN KEY (symbol)
REFERENCES stock_list(symbol);

-- ⚙️ Ràng buộc: trades ↔ stock_list
ALTER TABLE trades
ADD CONSTRAINT FK_trades_stock
FOREIGN KEY (symbol)
REFERENCES stock_list(symbol);
