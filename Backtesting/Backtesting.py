import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False

class Backtesting:
    def __init__(self,data):
        self.data = data

    def data_handling(self):
        self.data.index = pd.to_datetime(self.data.date)
        # self.data = self.data.drop(columns="date")
        self.data['portfolio_gain'] = self.data['portfolio_value'].pct_change()
        self.data['bitcoin_price_change'] = self.data['close'].pct_change()
        self.data = self.data.fillna(0)
        self.data['capital_line'] = (self.data.portfolio_gain + 1.0).cumprod()
        self.data['bitcoin_line'] = (self.data.bitcoin_price_change + 1.0).cumprod()


    def plot_performance(self):
        d1 = self.data[['capital_line','bitcoin_line']].copy()
        d1=d1.rename(columns={'capital_line':'策略累计净值','bitcoin_line':'bitcoin走势'})
        d1.plot(figsize=(15,7))
        plt.title('策略回测',size=15)
        plt.xlabel('')
        ax=plt.gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        plt.show()

    def performance(self):

        total_ret = self.data[['capital_line',  'bitcoin_line']].iloc[-1] - 1
        # timespan = datetime.strptime(self.data.iloc[-1,0], "%Y-%m-%d %H:%M:%S") - datetime.strptime(self.data.iloc[0,0],"%Y-%m-%d %H:%M:%S")
        # annual_ret = pow(1 + total_ret, 365*24*3600 / timespan.seconds) - 1
        #计算最大回撤
        dd = (self.data[['capital_line', 'bitcoin_line']].cummax() - \
              self.data[['capital_line', 'bitcoin_line']]) / \
             self.data[['capital_line', 'bitcoin_line']].cummax()
        d = dd.max()
        beta = self.data[['portfolio_gain', 'bitcoin_price_change']].cov().iat[0, 1] / self.data['bitcoin_price_change'].var()
        alpha = (total_ret['capital_line'] - total_ret['bitcoin_line'] * beta)
        exReturn = self.data['portfolio_gain'] - self.data['bitcoin_price_change']
        sharpe_ratio = np.sqrt(len(exReturn)) * exReturn.mean() / exReturn.std()
        TA1 = round(total_ret['capital_line'] * 100, 2)
        TA2 = round(total_ret['bitcoin_line'] * 100, 2)
        # AR1 = round(annual_ret['capital_line'] * 100, 2)
        # AR2 = round(annual_ret['bitcoin_line'] * 100, 2)
        MD1 = round(d['capital_line'] * 100, 2)
        MD2 = round(d['bitcoin_line'] * 100, 2)
        S = round(sharpe_ratio, 2)

        print(f'总收益率：  策略{TA1}%, 指数{TA2}%')
        # print(f'年化收益率：策略{AR1}%, 指数{AR2}%')
        print(f'最大回撤：  策略{MD1}%, 指数{MD2}%')
        print(f'策略Alpha： {round(alpha, 2)}, Beta：{round(beta, 2)}，夏普比率：{S}')
