import yfinance as yf
import datetime as dt
import numpy as np

ticker = "^GSPC"
start_date = dt.datetime.today() - dt.timedelta(1825)
end_date = dt.datetime.today()

data = yf.download(ticker, start_date, end_date)


def cagr(DF):
    df = DF.copy()
    df['daily_return'] = DF['Adj Close'].pct_change()
    df['cumulative_return'] = (1 + df.daily_return).cumprod()
    n = len(df) / 252  # this needs to change depending on what you're looking at in the trading period
    cagr = (df.cumulative_return[-1]) ** (1 / n) - 1

    return cagr

cagr = cagr(data)
cagr
