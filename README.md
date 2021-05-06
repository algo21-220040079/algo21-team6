# algo21-team6
Our team members and responsibility:
文皓平 220040079：
邓伟杰 
王冰
谢讯

Our system contains 7 parts:

  - craw (get data)
  - Feed (send data to our system)
  - Strategy (strategy module)
  - Portfollio (position management module)
  - Execution (order execution module)
  - Backtesting (draw backtesting graph)
  - main function
  
  ## craw
This module is a separate module. Running this craw.py, we will use an API called bittrex(https://api.bittrex.com/api/v1.1/public/getmarkethistory?market=usdt-btc) to get realtime bitcoin trading order. The to_dataframe.py perform the function that resamples the order flow to dataframe, which shows open,close,high,low and volume of trading price in a certain period (about 2-3mins,maybe has slightly difference). (btw: The time limit for getting is 60 requests per minute, so a time.sleep(1) is added.)

To save the data, we have two ways. One way is to implement MySQL database. But for convenience and data-sharing with teammates, we can also save in Json form and write it into txt. There are two txt flies, one is the complete transaction data(named data_all.txt) that includes details of each transaction, and the other(named data.txt) is open,close,high,low and volume of trading price in a certain period as mentioned above. 
In our craw module, the data.txt and data_all.txt have been saved, which show the data from 10a.m. May 4th to 10a.m. May 5th. In our later work, we will read the data.txt in our main function to start our whole backtesting system.

  ## Feed
This module is to transfer the transaction data to our system, connecting data and further analysis modules.  
(craw -> data -> Feed -> Strategy -> Portfolio -> Execution -> Backtesting)

  ## Strategy
This module is used to analyze the transaction data to predict the trend of price. Firstly it receives the transaction data from the Feed module. Secondly, it will analyze the transaction data through functions in Strategy module. Thirdly, it will sets buy_index (buy index) and sell_index (sell index). Lastly, it will transport the buy_index and the sell_index to Portfollio module.

  ## Portfollio
This module is used to manage position. Although we have judged the buying and selling trend, we need to limit the position. For example, we can set a limiting that the proportion of the position must less than 0.5. So, this module plays a limiting role. Then, the opening and selling signals will be sent to the next one--Execution module.

There are the meaning of some parameters:

buy_amount and sell_amount: It is a fixed rate to trade (In our setting, we start with principal 1 million, and we set this parameter to 100000)
trade_signal: It is a trading signal. The ‘sell’ is for sale. The ‘buy’ is for purchase. The ‘None’ is for inaction. In the subsequent code, that is a judgment basis.
judge_position: It is standard to judge position, and the value is less than 1.

  ## Execution
This module is used to execute an order to simulate the real situation about trading. And it will eventually return a total profit and loss. There are the meaning of some parameters:
tip: Handling fee.
buy_flap: The slippage of buying.
sell_flap: The slippage of selling.
buy_last_price and sell_last_price: the last price of trading.
Each transection will both print in the console and save in record.txt. 

  ## Backtesting
This module firstly draw the backtesting line of our strategy and the market price of Bitcoin, then calculate total return, maximum drawback, alpha, beta and Sharpe ratio of our strategy.



