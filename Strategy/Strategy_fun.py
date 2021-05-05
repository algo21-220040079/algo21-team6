import talib as ta
import numpy as np

def macd(data,index):
    close_arry = tranform_arry(data['close'])
    macd, macdsignal, macdhist = ta.MACD(close_arry, fastperiod=12, slowperiod=26, signalperiod=9)
    index['macd'] = {'macd':macd,'macdsignal':macdsignal,'macdhist':macdhist}

def ma(data,index):
    close_arry = tranform_arry(data['close'])
    index['ma'] = ta.MA(close_arry, timeperiod=10)

def tranform_arry(dataframe):
    close = [float(x) for x in dataframe]
    return np.array(close)

def add_features(data):
    data['MA13']=ta.MA(data.close,timeperiod=13)
    data['MA34']=ta.MA(data.close,timeperiod=34)
    data['MA89']=ta.MA(data.close,timeperiod=89)
    data['EMA10']=ta.EMA(data.close,timeperiod=10)
    data['EMA30']=ta.EMA(data.close,timeperiod=30)
    data['EMA200']=ta.EMA(data.close,timeperiod=200)
    data['MOM10']=ta.MOM(data.close,timeperiod=10)
    data['MOM30']=ta.MOM(data.close,timeperiod=30)
    data['RSI10']=ta.RSI(data.close,timeperiod=10)
    data['RSI30']=ta.RSI(data.close,timeperiod=30)
    data['RS200']=ta.RSI(data.close,timeperiod=200)
    data['K10'],data['D10']=ta.STOCH(data.high,data.low,data.close, fastk_period=10)
    data['K30'],data['D30']=ta.STOCH(data.high,data.low,data.close, fastk_period=30)
    data['K20'],data['D200']=ta.STOCH(data.high,data.low,data.close, fastk_period=200)