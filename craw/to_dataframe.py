import json
import pandas as pd
import time

def readfile(addr):
    result = []
    with open(addr, 'r') as r:
        for i in r.readlines():
            if (len(i) > 3):
                result.append(json.loads(i))
    return result

def to_dataframe(data):
    # 把数据转换为Dataframe格式
    result={"date":[],"open":[],"close":[],"low":[],"high":[],"volume":[]}
    for item in data:
        result["date"].append(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(item["data"])))
        result["open"].append(item["open_price"])
        result["close"].append(item["close"])
        result["low"].append(item["low"])
        result["high"].append(item["high"])
        result["volume"].append(item["volume"])
    df = pd.DataFrame(result)
    # df.index = pd.to_datetime(df.date)
    # df = df.drop(columns="date")
    df = df.round(2)

    return df

