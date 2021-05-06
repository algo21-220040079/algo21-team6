import requests
import json
import time
import pandas as pd
from sqlalchemy import create_engine

def craw(url):
    flag = True
    while flag:
        try:
            result = json.loads(requests.get(url,timeout = 3).text)
            flag = False
            return result
        except:
            flag = True
            time.sleep(1)


url5 = 'https://api.bittrex.com/v3/markets/BTC-USDT/trades'
history_id = []
history_oder = []
history_data = []
volume = 0.00
result = craw(url5)
open_price = result[0]['rate']
low = result[0]['rate']
high = result[0]['rate']
close = result[0]['rate']
volume += float(result[0]['quantity'])
history_id.append(result[0]['id'])
history_oder.append(result[0])

# 获取的时间限制是一分钟60次请求，所以会加上一个time.sleep(1)
time.sleep(1)
engine = create_engine('mysql+pymysql://root:root@localhost:3306/history_data')
number = 1
while True:
    result = craw(url5)
    for i in result:
        if i['id'] not in history_id:
            if(low>i['rate']):
                low = i['rate']
            if(high<i['rate']):
                high = i['rate']
            close = i['rate']
            volume += float(i['quantity'])
            history_id.append(i['id'])
            history_oder.append(i)
    data = {'getmarkethistory':history_oder}
    history_data.append(history_oder)
    history_oder = []
    number += 1
    if(number > 60):
        # df1 = pd.DataFrame(history_data)
        df2 = pd.DataFrame({'date':time.time(),'open_price':[open_price],'close':[close],'low':[low],'high':[high],'volume':[volume],'code':['btc']})
        # df1.to_sql('data_all', engine, if_exists='append', index=True)
        df2.to_sql('data', engine, if_exists='append', index=True)

        open_price = result[-1]['rate']
        close = result[-1]['rate']
        low = result[-1]['rate']
        high = result[-1]['rate']
        number = 0
        volume = 0.00
        volume += float(result[-1]['quantity'])
        history_data = []
        history_id = []
    print(data)
    time.sleep(1)