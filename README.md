# algo21-team6
Our team members and responsibility:  
  - 文皓平 220040079：Execution and Backtesting modules  
  - 邓伟杰 220040053：craw module and MySQL implementation  
  - 王冰220040082: Portfolio module  
  - 谢迅220040088: Strategy module  

Our system contains 7 parts:

  - craw (get data)
  - Feed (send data to our system)
  - Strategy (strategy module)
  - Portfollio (position management module)
  - Execution (order execution module)
  - Backtesting (draw backtesting graph)
  - main function
  
  ## craw
This module is a separate module. There are two folders, craw and craw_sql. Mostlty, they are the same. The programme in 
craw_sql can save the data in MySQL database directly. But for convenience and data-sharing with teammates, we can also save 
in Json form and write it into txt with the programme in craw.

Running this 'craw.py/craw_sql.py', we will use an API from bittrex exchange(https://api.bittrex.com/v3/markets/BTC-USDT/trades) 
to get realtime bitcoin trading order. The 'to_dataframe.py/read_sql.py' perform the function that resamples the order flow 
to dataframe, which shows open,close,high,low and volume of trading price in a certain period 
(in this programme we just set it about 2-3mins as default, you can change it into a higher frequency).
The folder craw_sql also has a programme named 'history_sql.py'. It can help you to get minutes, 5minutes and 1hour history data
from bittrex exchange.

When saving the data, we have two ways. One way is writing to table name 'data' and 'data_all' in MySQL database. We can 
also write it into data.txt and data_all.txt. The table 'data_all' is the complete transaction data that includes 
details of each transaction, and the 'data' is open,close,high,low and volume of trading price in a certain period as mentioned above. 
In our craw module, the 'data.txt' and 'data_all.txt' have been saved. The MySQL data are saved in folder 'Dump20210507'. 
In our later work, we will read the 'data' in our main function to start our whole backtesting system.

  ## Feed
This module is to transfer the transaction data to our system, connecting data and further analysis modules.  
(craw -> data -> Feed -> Strategy -> Portfolio -> Execution -> Backtesting)

  ## Strategy
This module is used to analyze the transaction data to predict the trend of price. Firstly it receives the transaction data from the Feed module. Secondly, it will analyze the transaction data through functions in Strategy module. Thirdly, it will make prediction (-1 or 1) based on analysis, and send such signals to Portfolio and Execution modules.

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



