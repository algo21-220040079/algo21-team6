import json
from pandas import DataFrame
from Feed.Feed import Feed
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from craw import to_dataframe


def backtest():
    """先运行craw模块获取数据，数据会自动保存到data.txt文件中，此处直接读取data.txt的数据。回测的时间段为运行craw模块的时间段"""
    result = to_dataframe.readfile(r'./craw/data.txt')
    data_frame = to_dataframe.to_dataframe(result)
    # dataframe格式，每2分钟的最高价、最低价、开盘价、收盘价、交易量、时间的数据。

    coin_number = 0  # 仓位拥有币数
    principal = 1000000  # 本金
    initials = {'coin_number': coin_number, 'principal': principal, 'initial_retail_price': result[0]['close']}
    # col = ['date', 'open_price', 'close', 'low', 'high', 'volume', 'code']
    # data_frame = DataFrame(columns=col)
    #
    # for i in result:
    #     data_frame = data_frame.append(i, ignore_index=True)
    feed = Feed(data_frame, coin_number, principal)
    msg = feed.send_data()  # 返回的是字典数据
    coin_number = msg['coin_number']
    principal = msg['principal']
    print('coin_number:' + str(coin_number) + ',principal:' + str((principal)))
    # last_retail_price = data_frame.iat[-1,2]
    # total_change_money = round((initials['coin_number'] * initials['initial_retail_price'] + initials['principal']) - (coin_number * last_retail_price + principal),3)
    # if(total_change_money>0):
    #     print('earn：' + str(total_change_money))
    # elif(total_change_money<0):
    #     print('lose：' + str(total_change_money))
    # elif(total_change_money == 0):
    #     print('balance')


def realtime_trading():
    import requests
    import time
    from multiprocessing import Manager, Pool, Pipe
    from craw.craw import craw

    url = 'https://api.bittrex.com/api/v1.1/public/getmarkethistory?market=usdt-btc'
    history_order = []
    history_id = []
    coin_number = 0  # 仓位拥有币数
    principal = 1000000  # 本金


    while(True):
        result = craw(url)['result']

        if result[0]['Id'] not in history_id:
            history_id.append(result[0]['Id'])
            history_order.append(result[0])
            print(result[0])

        time.sleep(0.5)
        if (len(history_order) > 20):
            print(history_order)
            col = ['Id', 'TimeStamp', 'Quantity', 'Price', 'Total', 'FillType', 'OrderType', 'Uuid']
            data_frame = DataFrame(columns=col)
            for i in history_order:
                data_frame = data_frame.append(i, ignore_index=True)
            data_frame = data_frame.rename(columns={"Price": "close","TimeStamp":"date"})

            feed = Feed(data_frame, coin_number, principal,False)
            msg = feed.send_data()
            print(msg)
            history_order = []
            history_id = []


    coin_number = msg['coin_number']
    principal = msg['principal']
    price = msg['close']
    # flag = True
    # while flag:
    #     try:
    #         result = json.loads(requests.get(url,timeout = 3).text)['result']['Last']
    #         flag = False
    #         price = result
    #     except:
    #         flag = True
    #
    # time.sleep(1)
    # coin_number = 0  # 仓位拥有币数
    # principal = 1000000  # 本金
    # init = coin_number * price + principal
    # print('initial money: ' + str(init))
    # print('current price:'+str(price))
    #
    #
    #
    # while True:
    #     parent_conn2, child_conn2 = Pipe()
    #     pool = Pool(processes=2)
    #     pool.apply_async(func=analyze, args=(child_conn2,))
    #     kk = parent_conn2.recv()
    #     history_order.append(kk)
    #     time.sleep(1)
    #     print(history_order)
    #     if (len(history_order) > 500):
    #         for i in range(10):
    #             history_order.pop(index=i)
    #     if (len(history_order) > 100):
    #         col = ['Id', 'TimeStamp', 'Quantity', 'Price', 'Total', 'FillType', 'OrderType', 'Uuid']
    #         data_frame = DataFrame(columns=col)
    #         for i in history_order:
    #             data_frame = data_frame.append(i, ignore_index=True)
    #         data_frame = data_frame.rename(columns={"Price": "close"})
    #         data_frame.to_csv('./try.csv')
    #         feed = Feed(data_frame, coin_number, principal)
    #         msg = feed.send_data()
    #         print(msg)
    #         coin_number = msg['coin_number']
    #         principal = msg['principal']
    #         price = msg['close']
    #         print('Profit or loss: ' + str(coin_number * price + principal - init))
    #
    # parent_conn2.close()
    # pool.close()
    # pool.join()


if __name__ == '__main__':
    backtest()
    # realtime_trading()




