-- 🏦 1. Bảng ngành
CREATE TABLE industry (
    industry_code NVARCHAR(20) PRIMARY KEY,
    [industry_name] NVARCHAR(100)
);

-- 🧾 2. Bảng danh sách cổ phiếu
CREATE TABLE stock_list (
    symbol NVARCHAR(10) PRIMARY KEY,
    [name] NVARCHAR(100),
    industry_code NVARCHAR(20),
    exchange NVARCHAR(10),
    FOREIGN KEY (industry_code) REFERENCES industry(industry_code)
);

-- 📈 3. Bảng giá lịch sử cổ phiếu
CREATE TABLE price_data (
    symbol NVARCHAR(10),
    trade_date DATE,
    [open] FLOAT,
    [high] FLOAT,
    [low] FLOAT,
    [close] FLOAT,
    volume BIGINT,
    PRIMARY KEY (symbol, trade_date),
    FOREIGN KEY (symbol) REFERENCES stock_list(symbol)
);

-- 📊 4. Bảng dữ liệu chỉ số thị trường (VNINDEX, VN30...)
CREATE TABLE index_data (
    index_code NVARCHAR(20),
    trade_date DATE,
    [open] FLOAT,
    [high] FLOAT,
    [low] FLOAT,
    [close] FLOAT,
    volume BIGINT,
    PRIMARY KEY (index_code, trade_date)
);

-- ⚠️ 5. Bảng tín hiệu kỹ thuật (BUY / SELL)
CREATE TABLE signals (
    symbol NVARCHAR(10),
    trade_date DATE,
    signal_type NVARCHAR(10),         -- BUY / SELL / HOLD
    description NVARCHAR(255),
    PRIMARY KEY (symbol, trade_date),
    FOREIGN KEY (symbol) REFERENCES stock_list(symbol)
);

-- 💼 6. Bảng ghi nhật ký giao dịch
CREATE TABLE trades (
    trade_id INT IDENTITY(1,1) PRIMARY KEY,
    symbol NVARCHAR(10),
    trade_date DATE,                  -- Ngày thực hiện lệnh
    action NVARCHAR(10),             -- BUY / SELL
    quantity INT,
    entry_price FLOAT,
    exit_price FLOAT,
    exit_date DATE,
    pnl AS (exit_price - entry_price), -- Lãi/lỗ tự tính (computed column)
    strategy NVARCHAR(50),            -- Ví dụ: "Ichimoku-RSI"
    success BIT,                      -- 1: win, 0: loss
    note NVARCHAR(255),
    FOREIGN KEY (symbol) REFERENCES stock_list(symbol)
);
