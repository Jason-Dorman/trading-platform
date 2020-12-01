import yfinance as yf
import numpy as np
import datetime as dt

ticker = 'AAPL'
start_date = dt.datetime.today() - dt.timedelta(1825)
end_date = dt.datetime.today()

data = yf.download(ticker, start_date, end_date)


def obv(DF):
    # function to calculate on balance value
    df = DF.copy()
    df['daily_return'] = df['Adj Close'].pct_change() #calculate percent change in close
    df['direction'] = np.where(df.daily_return >= 0, 1, -1) # gives you positive, negative, or neutral change
    df.direction[0] = 0
    df['vol_adj'] = df.Volume * df.direction
    df['obv'] = df.vol_adj.cumsum() # find the cumulative sum
    return df


return_data = obv(data)
return_data
