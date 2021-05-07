from Execution.Execution import Execution
from Backtesting.Backtesting import Backtesting
import pandas as pd


class Portfollio:
    def __init__(self,coin_number,principal,data,backtest):
        self.coin_number = coin_number
        self.principal = principal
        self.buy_amount = 50000
        self.sell_amount = 50000
        self.data = data
        self.temp_data = self.data[0:1]
        self.trade_sigle = 'None'
        self.position = ( coin_number * self.data.iat[0,2] ) / ( self.principal + ( coin_number * self.data.iat[0,2] ) )
        self.judge_position = 0.5
        self.backtest = backtest

    def position_control(self):

        self.data['position'] = None
        self.data['coin_number'] =None
        self.data['principal'] = None
        self.data['portfolio_value'] = None

        if self.backtest:
            for indx, row in self.data.iterrows():
                self.temp_data = self.data[0:indx+1] #随着时间推移，获得更多数据
                self.position = (self.coin_number * self.temp_data.iat[-1, 2]) / (self.principal + (self.coin_number * self.temp_data.iat[-1, 2]))
                self.data.loc[indx, 'position'] = self.position
                if row['y_pred']>0 and self.judge_position > self.position:
                    self.buy()
                if row['y_pred']<0 and self.position>0:
                    self.sell()
                # if((row['buy_index'] > 0) and (row['buy_index'] > row['sell_index']) and (self.judge_position > self.position)):
                #     self.buy()
                # if((row['sell_index'] > 0) and (row['sell_index'] > row['buy_index']) and (self.position>0)):
                #     self.sell()
                self.data.loc[indx,'coin_number'] = self.coin_number
                self.data.loc[indx,'principal'] = self.principal
                self.data.loc[indx,'portfolio_value'] = self.coin_number*self.data.loc[indx,'close'] + self.principal

            self.data.to_csv("./回测期间比特币行情与量化指标数据.csv")
            backtesting = Backtesting(self.data)
            backtesting.data_handling()
            backtesting.plot_performance()
            backtesting.performance()
        else:
            self.temp_data = self.data.iloc[-1,:]  # 随着时间推移，获得更多数据
            self.position = (self.coin_number * self.temp_data.iat[-1, 3]) / (
                        self.principal + (self.coin_number * self.temp_data.iat[-1, 3]))
            if ((self.temp_data['buy_index'][0] > 0) and (self.temp_data['buy_index'][0] > self.temp_data['sell_index'][0]) and (
                    self.judge_position > self.position)):
                self.buy()
            if ((self.temp_data['sell_index'][0] > 0) and (self.temp_data['sell_index'][0] > self.temp_data['buy_index'][0]) and (self.position > 0)):
                self.sell()

        return {'coin_number':self.coin_number,'principal':self.principal}

    def buy(self):
        signal = 'buy'
        self.Execution = Execution(signal,self.buy_amount,self.sell_amount,self.temp_data,self.principal,self.coin_number)
        result = self.Execution.excu()
        self.coin_number = result['coin_number']
        self.principal = result['principal']

    def sell(self):
        signal = 'sell'
        sell_amount = self.sell_amount
        if(self.sell_amount > self.coin_number*self.temp_data.iat[-1, 2]):
            sell_amount = self.coin_number/2*self.temp_data.iat[-1, 2]
        self.Execution = Execution(signal,self.buy_amount,sell_amount,self.temp_data,self.principal,self.coin_number)
        result = self.Execution.excu()
        self.coin_number = result['coin_number']
        self.principal = result['principal']

