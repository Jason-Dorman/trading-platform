import yfinance as yf
import datetime as dt
from stocktrends import Renko
from app.atr_bb_example import atr


class SetUp:
    ticker = 'AAPL'
    start_date = dt.datetime.today() - dt.timedelta(364)
    end_date = dt.datetime.today()

    data = yf.download(ticker, start_date, end_date)


def transform_data(data):
    # have to transform data to use stocktrends Renko. Uses adjusted close as close
    df = data.copy()
    df.reset_index(inplace=True)
    df = df.iloc[:, [0, 1, 2, 3, 5, 6]]
    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

    return df


def renko():
    renko_data = Renko(transform_data(SetUp.data))
    renko_data.brick_size = round(atr(SetUp.data, 120)['ATR'][-1], 0)
    renko_df = renko_data.get_ohlc_data()

    return renko_df

#ToDo create a renko chart
renko = renko()
renko
