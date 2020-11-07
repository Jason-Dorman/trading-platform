import pandas as pd
import datetime as dt
import yfinance as yf


stocks = ["AAPL", "MSFT"]
start_date = dt.datetime.today() - dt.timedelta(30)
end_date = dt.datetime.today()

cl_price = pd.DataFrame()
full_data = {}

for stock in stocks:
    cl_price[stock] = yf.download(stock, start_date, end_date)['Adj Close']

for stock in stocks:
    full_data[stock] = yf.download(stock, start_date, end_date)


class next:
    pass

