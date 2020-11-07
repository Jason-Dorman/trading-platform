import datetime as dt
import yfinance as yf

ticker = "AAPL"
start_date = dt.datetime.today() - dt.timedelta(1825)
end_date = dt.datetime.today()

data = yf.download(ticker, start_date, end_date)


def atr(DF, n):
    # calculate true range and average true range (n=20)
    ohlcv = DF.copy()
    ohlcv['H-L'] = abs(ohlcv['High'] - ohlcv['Low'])
    ohlcv['H-PC'] = abs(ohlcv['High'] - ohlcv['Adj Close'].shift(1))
    ohlcv['L-PC'] = abs(ohlcv['Low'] - ohlcv['Adj Close'].shift(1))
    ohlcv['True_Range'] = ohlcv[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)
    ohlcv['ATR'] = ohlcv['True_Range'].rolling(n).mean()
    ohlcv.dropna(inplace=True)
    return ohlcv


def bollingerBand(DF, n):
    # calculate Bollinger Band (n=20)
    ohlcv = DF.copy()
    ohlcv['MA'] = ohlcv['Adj Close'].rolling(n).mean()
    ohlcv['BB_over'] = ohlcv['MA'] + 2 * ohlcv['MA'].rolling(n).std()
    ohlcv['BB_under'] = ohlcv['MA'] - 2 * ohlcv['MA'].rolling(n).std()
    ohlcv['BB_difference'] = ohlcv['BB_over'] - ohlcv['BB_under']
    ohlcv.dropna(inplace=True)
    return ohlcv


bollingerBand(data, 20).iloc[-100:, [-4, -3, -2]].plot()
