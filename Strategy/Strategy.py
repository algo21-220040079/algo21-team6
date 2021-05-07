from Portfollio.Portfollio import Portfollio
from multiprocessing import  Manager,Pool
import talib as ta
import numpy as np

class Strategy:
    def __init__(self,data,coin_number,principal,backtest):
        self.buy_index = 0
        self.sell_index = 0
        self.coin_number = coin_number
        self.principal = principal
        self.data = data
        self.backtest = backtest

    def analysis(self):
        add_features(self.data)
        y = np.where(self.data.close.pct_change().shift(-1) > 0, 1, -1)
        self.data['next_signal'] = y
        train = self.data.iloc[:100,:] #以前100组数据为训练集
        train = train.dropna()
        from xgboost import XGBClassifier
        model = XGBClassifier(n_estimators=25)
        X = train[['volume','ma', 'macd','macdsignal','macdhist','MOM10', 'K10', 'D10']]
        y = train[['next_signal']]
        model.fit(X,y)
        test = self.data.iloc[100:, :]
        test.to_csv('./测试集详细数据.csv')
        X_test = test[['volume','ma', 'macd','macdsignal','macdhist','MOM10', 'K10', 'D10']]
        y_pred = model.predict(X_test)
        test['y_pred'] = y_pred
        test.to_csv('./2.csv')
        self.Portfollio = Portfollio(self.coin_number,self.principal,test,self.backtest)

        #下面是旧策略，效果不佳，注释于此
        # for  indx, row in self.data.iterrows():
        #     if(row['macdhist']>0):
        #         self.buy_index_adjust(60)
        #     if(row['macdhist']<0):
        #         self.sell_index_adjust(60)
        #
        #     if(row['close']>row['ma']):
        #         self.buy_index_adjust(40)
        #     if(row['close']<row['ma']):
        #         self.sell_index_adjust(40)
        #     record[0]['buy_index'].append(self.buy_index)
        #     record[1]['sell_index'].append(self.sell_index)
        #     self.buy_index = 0
        #     self.sell_index = 0
        # self.data['buy_index'] = np.array(record[0]['buy_index'])
        # self.data['sell_index'] = np.array(record[1]['sell_index'])
        # self.Portfollio = Portfollio(self.coin_number,self.principal,self.data,self.backtest)
        return self.Portfollio.position_control()

    # def analysis(self):
    #     with Manager() as manager:
    #         index = manager.dict()
    #         pool = Pool(processes=2)
    #         pool.apply_async(func=macd,args=(self.data,index))
    #         pool.apply_async(func=ma, args=(self.data, index))
    #         pool.close()
    #         pool.join()
    #         ######判断参数条件
    #         self.data['macd'] = index['macd']['macd']
    #         self.data['macdhist'] = index['macd']['macdhist']
    #         self.data['macdsignal'] = index['macd']['macdsignal']
    #         self.data['ma'] = index['ma']
    #         recod = [{'buy_index':[]},{'sell_index':[]}]#初始化装buy_index和sell_index 的列表
    #         for  indx, row in self.data.iterrows():
    #             if(row['macdhist']>0):
    #                 self.buy_index_adjust(60)
    #             if(row['macdhist']<0):
    #                 self.sell_index_adjust(60)
    #
    #             if(row['close']>row['ma']):
    #                 self.buy_index_adjust(40)
    #             if(row['close']<row['ma']):
    #                 self.sell_index_adjust(40)
    #             recod[0]['buy_index'].append(self.buy_index)
    #             recod[1]['sell_index'].append(self.sell_index)
    #             self.buy_index = 0
    #             self.sell_index = 0
    #         self.data['buy_index'] = np.array(recod[0]['buy_index'])
    #         self.data['sell_index'] = np.array(recod[1]['sell_index'])
    #         add_features(self.data)
    #         self.Portfollio = Portfollio(self.coin_number,self.principal,self.data)
    #         return self.Portfollio.position_control()


    def buy_index_adjust(self,number):
        self.buy_index += number

    def sell_index_adjust(self,number):
        self.sell_index += number


def tranform_arry(dataframe):
    close = [float(x) for x in dataframe]
    return np.array(close)


def macd(data, index):
    close_arry = tranform_arry(data['close'])
    macd, macdsignal, macdhist = ta.MACD(close_arry, fastperiod=12, slowperiod=26, signalperiod=9)
    index['macd'] = {'macd': macd, 'macdsignal': macdsignal, 'macdhist': macdhist}

def ma(data, index):
    close_arry = tranform_arry(data['close'])
    index['ma'] = ta.MA(close_arry, timeperiod=10)

def add_features(data):
    data['macd'], data['macdsignal'], data['macdhist'] = ta.MACD(data.close,fastperiod=6, slowperiod=12, signalperiod=9)
    data['ma']=ta.MA(data.close,timeperiod=10)
    # data['MA34']=ta.MA(data.close,timeperiod=34)
    # data['MA89']=ta.MA(data.close,timeperiod=89)
    # data['EMA10']=ta.EMA(data.close,timeperiod=10)
    # data['EMA30']=ta.EMA(data.close,timeperiod=30)
    # data['EMA200']=ta.EMA(data.close,timeperiod=200)
    data['MOM10']=ta.MOM(data.close,timeperiod=10)
    # data['MOM30']=ta.MOM(data.close,timeperiod=30)
    # data['RSI10']=ta.RSI(data.close,timeperiod=10)
    # data['RSI30']=ta.RSI(data.close,timeperiod=30)
    # data['RS200']=ta.RSI(data.close,timeperiod=200)
    data['K10'],data['D10']=ta.STOCH(data.high,data.low,data.close, fastk_period=10)
    # data['K30'],data['D30']=ta.STOCH(data.high,data.low,data.close, fastk_period=30)
    # data['K20'],data['D200']=ta.STOCH(data.high,data.low,data.close, fastk_period=200)
