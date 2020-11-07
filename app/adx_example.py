import yfinance as yf
import datetime as dt
import numpy as np
from app.atr_bb_example import atr

# TODO create a setup class/ function to call in all technical indicator functions
ticker = "AAPL"
start_date = dt.datetime.today() - dt.timedelta(364)
end_date = dt.datetime.today()

data = yf.download(ticker, start_date, end_date)


def adx(DF, n):
    stock_data = DF.copy()
    stock_data['TR'] = atr(data, n)['True_Range']
    stock_data['Directional_Movement_Index_pos'] = np.where(
        (stock_data.High - stock_data.High.shift(1)) > (stock_data.Low.shift(1) - stock_data.Low),
        stock_data.High - stock_data.High.shift(1), 0)
    stock_data.Directional_Movement_Index_pos = np.where(stock_data.Directional_Movement_Index_pos < 0, 0,
                                                         stock_data.Directional_Movement_Index_pos)
    stock_data['Directional_Movement_Index_neg'] = np.where(
        (stock_data.Low - stock_data.Low.shift(1)) > (stock_data.High.shift(1) - stock_data.High),
        stock_data.Low - stock_data.Low.shift(1), 0)
    stock_data.Directional_Movement_Index_neg = np.where(stock_data.Directional_Movement_Index_neg < 0, 0,
                                                         stock_data.Directional_Movement_Index_neg)
    true_rangeN = []
    dmi_plusN = []
    dmi_minusN = []
    true_range = stock_data.TR.tolist()
    dmi_plus = stock_data.Directional_Movement_Index_pos.tolist()
    dmi_minus = stock_data.Directional_Movement_Index_neg.tolist()

    for i in range(len(stock_data)):
        if i < n:
            true_rangeN.append(np.NaN)
            dmi_plusN.append(np.NaN)
            dmi_minusN.append(np.NaN)
        elif i == n:
            true_rangeN.append(stock_data.TR.rolling(n).sum().tolist()[n])
            dmi_plusN.append(stock_data.Directional_Movement_Index_pos.rolling(n).sum().tolist()[n])
            dmi_minusN.append(stock_data.Directional_Movement_Index_neg.rolling(n).sum().tolist()[n])
        elif i > n:
            true_rangeN.append(true_rangeN[i - 1] - (true_rangeN[i - 1] / 14) + true_range[i])
            dmi_plusN.append(dmi_plusN[i - 1] - (dmi_plusN[i - 1] / 14) + dmi_plus[i])
            dmi_minusN.append(dmi_minusN[i - 1] - (dmi_minusN[i - 1] / 14) + dmi_minus[i])

    stock_data['true_rangeN'] = np.array(true_rangeN)
    stock_data['dmi_plusN'] = np.array(dmi_plusN)
    stock_data['dmi_minusN'] = np.array(dmi_minusN)


    return stock_data


return_data = adx(data, 14)

return_data
