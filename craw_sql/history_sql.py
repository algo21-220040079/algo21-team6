import requests
import json
import time
import pandas as pd
from sqlalchemy import create_engine


def craw(url):  # 读取json文件
    flag = True
    while flag:
        try:
            result = json.loads(requests.get(url,timeout = 3).text)
            flag = False
            return result
        except:
            flag = True
            time.sleep(1)


def update_data(table_name, sql_password):  # 提供不同频率数据的抓取和写入
    url5 = {'old_his':'https://api.bittrex.com/api/v1.1/public/getmarkethistory?market=usdt-btc',
            'new_his':'https://api.bittrex.com/v3/markets/BTC-USDT/trades',
            'day': 'https://api.bittrex.com/v3/markets/BTC-USDT/candles/DAY_1/recent',
            'hour':'https://api.bittrex.com/v3/markets/BTC-USDT/candles/HOUR_1/recent',
            'minute5': 'https://api.bittrex.com/v3/markets/BTC-USDT/candles/MINUTE_5/recent',
            'minute':'https://api.bittrex.com/v3/markets/BTC-USDT/candles/MINUTE_1/recent',
            }

    data = craw(url5[table_name])  # 获取最新数据
    df1 = pd.DataFrame(data)

    # 连接mysql
    engine = create_engine('mysql+pymysql://root:{0}@localhost:3306/history_data'.format(sql_password))


    try:
        # 增量更新
        sql = '''select * from {0} ORDER BY startsAt DESC LIMIT 1;'''.format(table_name)
        df2 = pd.read_sql_query(sql, engine)
        i = df1.loc[df1.startsAt == df2.loc[0, 'startsAt']].index
        df_app = df1.loc[i[0] + 1:]
        df_app = df_app.reset_index(drop=True)
        df_app.index = df_app.index + df2.loc[0, 'index'] + 1
        df_app.to_sql(table_name, engine, if_exists='append', index=True)
        print('Append to Mysql table {0} successfully!'.format(table_name))
        # 全量更新
        # sql = ''' select * from {0}; '''.format(table_name)
        # df2 = pd.read_sql_query(sql, engine).drop(['index'], axis=1)
        # df2 = df2[:-1]
        # df_new = pd.concat([df2, df1], axis=0, ignore_index=True, copy=True)
        # df_new = df_new.drop_duplicates(keep='last', inplace=False)
        # df_new = df_new.reset_index(drop=True)
        # df_new.to_sql(table_name, engine, if_exists='replace', index=True)
        # print('Write to Mysql table {0} successfully!'.format(table_name))
    except:
        df_new = df1
        df_new.to_sql(table_name, engine, if_exists='replace', index=True)
        print('Creat Mysql table {0} successfully!'.format(table_name))


def get_data(table_name, sql_password):     # 提取数据为df
    engine = create_engine('mysql+pymysql://root:{0}@localhost:3306/history_data'.format(sql_password))
    sql = ''' select * from {0}; '''.format(table_name)
    df = pd.read_sql_query(sql, engine).drop(['index'], axis=1)
    return df


if __name__ == '__main__':

    password = str('root')      #数据库root密码
    update_data('minute', password)
    update_data('minute5', password)
    update_data('hour', password)