import requests
import json
import time

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
        with open('data_all.txt','a') as w:
            w.write(json.dumps(history_data)+'\n')
        with open('data.txt','a') as ws:
            ws.write(json.dumps({'data':time.time(),'open_price':open_price,'close':close,'low':low,'high':high,'volume':volume,'code':'btc'})+'\n')
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