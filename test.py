import yfinance as yf

ticker = yf.Ticker("NVDA")
info = ticker.info
print("-"*55)
print(info)
print("-"*55)

