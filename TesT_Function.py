from vnstock import Quote
q = Quote(symbol='FPT')

df = q.intraday(date='2025-06-17', resolution='1')  # <- nếu 'intraday' là hàm tồn tại
print(df.tail())