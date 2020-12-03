import yfinance as yf
import numpy as np
import datetime as dt
import statsmodels.api as sm
import matplotlib.pyplot as plt

ticker = 'AAPL'
start_date = dt.datetime.today() - dt.timedelta(365)
end_date = dt.datetime.today()

data = yf.download(ticker, start_date, end_date)


def consecutive_slope(ser,
                      n):  # ser is a numpy series can change to df if needed/wanted. n is number of consectuvie points of adjusted close can change to higher number for longer view period
    # calculates slope of regression line for n consecutive points
    slopes = [i * 0 for i in range(n - 1)]
    for i in range(n, len(ser) + 1):
        # range never includes last value so you add one to include that last value
        y = ser[i - n:i]
        X = np.array(range(n))
        y_scaled = (y - y.min()) / (y.max() - y.min())
        x_scaled = (X - X.min()) / (X.max() - X.min())
        x_scaled = sm.add_constant(x_scaled)
        model = sm.OLS(y_scaled, x_scaled)
        results = model.fit()
        slopes.append(results.params[-1])
    slope_angle = (np.rad2deg(np.arctan(np.array(slopes))))
    return np.array(slope_angle)


def previous_slope(ser, n):
    # calculates slope of line connecting a point with n-previous point. Slope assumes a frame with 22 units in the x
    # axis and span of min to max in y axis
    y_span = ser.max() - ser.min()
    x_span = 22
    slopes = [i * 0 for i in range(n - 1)]
    for i in range(n - 1, len(ser)):
        y2 = ser[i]
        y1 = ser[i - n + 1]
        slope = ((y2 - y1) / y_span) / (n / x_span)
        slopes.append(slope)
    slope_angle = (np.rad2deg(np.arctan(np.array(slopes))))
    return np.array(slope_angle)


df = data.copy()
df['slopes'] = consecutive_slope(data['Adj Close'], 5)

plot = df.iloc[:, [4, 6]].plot(subplots=True, layout=(2, 1))
