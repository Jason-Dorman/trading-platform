import datetime as dt
import yfinance as yf

ticker = "MSFT"
start_date = dt.datetime.today() - dt.timedelta(1825)
end_date = dt.datetime.today()

data = yf.download(ticker, start_date, end_date)


def macd(DF, fast, slow, signal): # macd(data, 12, 26, 9)
    # calculate fast and slow moving averages - 'span' is param for ewm method for what MA you want to use
    ohlcv = DF.copy()
    ohlcv['MA_fast'] = ohlcv['Adj Close'].ewm(span=fast, min_periods=fast).mean()
    ohlcv['MA_slow'] = ohlcv['Adj Close'].ewm(span=slow, min_periods=slow).mean()
    ohlcv['MACD'] = ohlcv['MA_fast'] - ohlcv['MA_slow']
    ohlcv['Signal'] = ohlcv['MACD'].ewm(span=signal, min_periods=signal).mean()
    ohlcv.dropna(inplace=True)
    return ohlcv


macd(data, 12, 26, 9)

# TODO plot