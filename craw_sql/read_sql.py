import pandas as pd
from sqlalchemy import create_engine
import time

def get_data(table_name, sql_password):     # 提取数据为df
    engine = create_engine('mysql+pymysql://root:{0}@localhost:3306/history_data'.format(sql_password))
    sql = ''' select * from {0}; '''.format(table_name)
    if table_name == 'data':
        df = pd.read_sql_query(sql, engine).drop(['index','code'], axis=1)
        df['date'] = pd.to_datetime(df['date'],unit='s')
        df1 = df.iloc[:, 0:1]
        df2 = df.iloc[:, 1:].astype(float)
        df = pd.concat([df1, df2], axis=1)
    else:
        df = pd.read_sql_query(sql, engine).drop(['index','quoteVolume'], axis=1)
        df.rename(index=str, columns={"startsAt": "date"}, inplace=True)
        df1 = df.iloc[:, 0:1]
        df2 = df.iloc[:, 1:].astype(float)
        df = pd.concat([df1, df2], axis=1)

    return df



if __name__ == '__main__':
    password = str('root')      #数据库root密码
    table = str('data')
    get_data(table, password)
