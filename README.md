# algo21-team6

Our system contains 7 parts:

  -craw (get data)  
  -Feed (send data to our system)  
  -Strategy (strategy module)
  -Portfollio (position management module)
  -Execution (order execution module)
  -Backtesting (draw backtesting graph)
  -main function
## craw
This module is a separate module. Running this craw.py, we will use an API called bittrex(https://api.bittrex.com/api/v1.1/public/getmarkethistory?market=usdt-btc) to get realtime bitcoin trading order. The to_dataframe.py perform the function that resamples the order flow to dataframe, which shows open,close,high,low and volume of trading price in a certain period (about 2-3mins,maybe has slightly difference). (btw: The time limit for getting is 60 requests per minute, so a time.sleep(1) is added.)

To save the data, we have two ways. One way is to implement MySQL database. But for convenience and data-sharing with teammates, we can also save in Json form and write it into txt. There are two txt flies, one is the complete transaction data(named data_all.txt) that includes details of each transaction, and the other(named data.txt) is open,close,high,low and volume of trading price in a certain period as mentioned above. 
In our craw module, the data.txt and data_all.txt have been saved, which show the data from 10a.m. May 4th to 10a.m. May 5th. In our later work, we will read the data.txt in our main function to start our whole backtesting system.


  1.文本1
  2.文本2

# 一级标题
## 二级标题
### 三级标题

