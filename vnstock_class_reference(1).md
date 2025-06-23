
# Tổng hợp Class và Method của thư viện `vnstock`

Dưới đây là danh sách các class chính trong thư viện `vnstock`, cùng với mô tả chức năng và ví dụ sử dụng cơ bản.

---

## 🔹 1. `Listing`

### 📘 Chức năng:
Lấy danh sách các công ty đang niêm yết, UPCOM hoặc đã hủy niêm yết.

### 📥 Method:
- `get_listed_companies()`: Trả về danh sách công ty niêm yết.

### 💡 Ví dụ:
```python
from vnstock import Listing

ls = Listing()
df = ls.get_listed_companies()
print(df.head())
```

---

## 🔹 2. `Company`

### 📘 Chức năng:
Lấy thông tin chi tiết về công ty như hồ sơ doanh nghiệp, ngành nghề, sở hữu, v.v.

### 📥 Method:
- `get_company_overview(symbol: str)`

### 💡 Ví dụ:
```python
from vnstock import Company

cp = Company()
info = cp.get_company_overview("MWG")
print(info)
```

---

## 🔹 3. `Quote`

### 📘 Chức năng:
Truy xuất thông tin giá cổ phiếu hiện tại, giá trần/sàn/đóng cửa.

### 📥 Method:
- `get_quote(symbol: str)`

### 💡 Ví dụ:
```python
from vnstock import Quote

qt = Quote()
price = qt.get_quote("FPT")
print(price)
```

---

## 🔹 4. `Trading`

### 📘 Chức năng:
Truy xuất dữ liệu giao dịch, giá intraday, khối lượng, lịch sử.

### 📥 Method:
- `get_intraday_prices(symbol: str, page: int = 0)`
- `get_historical_prices(symbol: str, start_date: str, end_date: str, resolution: str)`

### 💡 Ví dụ:
```python
from vnstock import Trading

tr = Trading()
df = tr.get_intraday_prices("SSI")
print(df.head())
```

---

## 🔹 5. `Finance`

### 📘 Chức năng:
Truy xuất báo cáo tài chính, cân đối kế toán, dòng tiền, lợi nhuận.

### 📥 Method:
- `get_financial_ratios(symbol: str)`
- `get_income_statement(symbol: str)`
- `get_balance_sheet(symbol: str)`
- `get_cash_flow(symbol: str)`

### 💡 Ví dụ:
```python
from vnstock import Finance

fin = Finance()
ratios = fin.get_financial_ratios("VNM")
print(ratios.head())
```

---

## 🔹 6. `Fund`

### 📘 Chức năng:
Dữ liệu quỹ đầu tư, ETF, danh mục nắm giữ.

---

## 🔹 7. `Screener`

### 📘 Chức năng:
Lọc cổ phiếu theo tiêu chí định sẵn như P/E, EPS, ROE...

---

## 🔹 8. `Vnstock` (Tổng hợp)

### 📘 Chức năng:
Class tổng hợp tất cả các class con (Listing, Company, Trading, ...)

### 💡 Ví dụ:
```python
from vnstock import Vnstock

vs = Vnstock()
data = vs.trading.get_intraday_prices("VCB")
print(data.head())
```

---

## 📝 Ghi chú

- Thư viện hỗ trợ lấy dữ liệu từ nhiều nguồn: VCI, TCBS, MSN...
- Các class theo chuẩn Python Wrapper, bạn phải tạo đối tượng trước khi dùng method.
- Dữ liệu trả về thường là DataFrame (pandas), dễ dàng xử lý, thống kê.

---

## 🧠 Đề xuất

Nên sử dụng Jupyter hoặc VSCode với tính năng auto-complete để trải nghiệm tốt nhất.

---

# 🚀 Ví dụ nâng cao với `vnstock`

Dưới đây là một số ví dụ nâng cao giúp bạn tận dụng tối đa thư viện `vnstock` để phân tích dữ liệu cổ phiếu và trực quan hóa bằng biểu đồ.

---

## 📊 1. Vẽ biểu đồ giá cổ phiếu Intraday

```python
from vnstock import Trading
import matplotlib.pyplot as plt

# Lấy dữ liệu giao dịch intraday
tr = Trading()
df = tr.get_intraday_prices("FPT")

# Chuyển đổi cột datetime nếu cần
df["time"] = pd.to_datetime(df["time"])

# Vẽ biểu đồ
plt.figure(figsize=(12, 6))
plt.plot(df["time"], df["price"], label="Giá")
plt.title("Biểu đồ giá Intraday - FPT")
plt.xlabel("Thời gian")
plt.ylabel("Giá")
plt.legend()
plt.grid(True)
plt.show()
```

---

## 📈 2. Vẽ biểu đồ lịch sử giá đóng cửa

```python
from vnstock import Trading
import matplotlib.pyplot as plt

tr = Trading()
df = tr.get_historical_prices("MWG", start_date="2024-01-01", end_date="2024-06-01", resolution="1D")

# Đảm bảo cột datetime
df["datetime"] = pd.to_datetime(df["datetime"])

# Vẽ
plt.figure(figsize=(10, 5))
plt.plot(df["datetime"], df["close"], label="Giá đóng cửa", color="green")
plt.title("Lịch sử giá đóng cửa MWG")
plt.xlabel("Ngày")
plt.ylabel("Giá đóng cửa")
plt.grid(True)
plt.legend()
plt.show()
```

---

## 🔍 3. Lọc cổ phiếu theo tiêu chí (Screener)

```python
from vnstock import Screener

sc = Screener()
# Ví dụ lọc cổ phiếu có P/E < 15 và ROE > 10%
criteria = {
    "pe_ratio": {"operator": "<", "value": 15},
    "roe": {"operator": ">", "value": 10}
}
df = sc.filter_stocks(criteria)
print(df.head())
```

---

## 📊 4. So sánh các cổ phiếu cùng ngành

```python
from vnstock import Quote
import pandas as pd
import matplotlib.pyplot as plt

symbols = ["FPT", "VGI", "CMG"]
qt = Quote()
data = []

for sym in symbols:
    q = qt.get_quote(sym)
    data.append({"symbol": sym, "price": q["price"], "change": q["percent_change"]})

df = pd.DataFrame(data)

# Vẽ biểu đồ cột so sánh
plt.figure(figsize=(8, 4))
plt.bar(df["symbol"], df["change"])
plt.title("So sánh phần trăm thay đổi giá cổ phiếu")
plt.ylabel("% thay đổi")
plt.grid(True)
plt.show()
```

---

## 🧠 Lưu ý thêm

- Dữ liệu từ `vnstock` là thời gian thực hoặc gần thời gian thực, phù hợp để dashboard theo dõi cổ phiếu.
- Có thể kết hợp với `plotly`, `streamlit`, `dash` để làm giao diện trực quan, dashboard.

