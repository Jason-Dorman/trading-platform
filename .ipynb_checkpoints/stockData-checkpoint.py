from app.key import key
import pandas as pd
import datetime as dt
import quandl

stocks = ["WIKI/AAPL", "WIKI/MSFT"]
start_date = dt.datetime.today() - dt.timedelta(30)
end_date = dt.datetime.today()
cl_price = pd.DataFrame()

quandl.ApiConfig.api_key = key

for stock in stocks:
    cl_price = quandl.get(stock, start_date=start_date, end_date=end_date)

cl_price.head()

