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


