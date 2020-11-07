import yfinance as yf
import datetime as dt
import numpy as np
import pandas as pd

ticker = "AAPL"
start_date = dt.datetime.today() - dt.timedelta(364)
end_date = dt.datetime.today()

data = yf.download(ticker, start_date, end_date)


def rsi(DF, n):
    # n is number of periods we cant to calculate the RSI
    # function to calculate RSI
    stock_data = DF.copy()
    stock_data['delta'] = stock_data['Adj Close'] - stock_data['Adj Close'].shift(1)  # find change in close price day over day
    stock_data['gain'] = np.where(stock_data['delta'] >= 0, stock_data['delta'],
                          0)  # np.where is an if/ then statement using the two parameters
    stock_data['loss'] = np.where(stock_data['delta'] < 0, abs(stock_data['delta']), 0)
    avg_gain = []
    avg_loss = []
    gain = stock_data['gain'].tolist()  # converting gain/loss to a list
    loss = stock_data['loss'].tolist()

    for i in range(len(stock_data)):
        if i < n:
            avg_gain.append(np.NaN)
            avg_loss.append(np.NaN)
        elif i == n:
            avg_gain.append(stock_data['gain'].rolling(n).mean().tolist()[n])
            avg_loss.append(stock_data['loss'].rolling(n).mean().tolist()[n])
        elif i > n:
            avg_gain.append(((n - 1) * avg_gain[i - 1] + gain[i]) / n)
            avg_loss.append(((n - 1) * avg_loss[i - 1] + loss[i]) / n)

    stock_data['avg_gain'] = np.array(avg_gain)  # appending the average list from above to a df column
    stock_data['avg_loss'] = np.array(avg_loss)
    stock_data['RS'] = stock_data['avg_gain'] / stock_data['avg_loss']
    stock_data['RSI'] = 100 - (100 / (1 + stock_data['RS']))

    return stock_data


stock_results = rsi(data, 14)

stock_results
