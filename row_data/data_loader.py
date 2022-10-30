from operator import index
import yfinance as yf
import requests
import numpy as np
import pandas as pd
import sys
from pathlib import Path
import os
import datetime as dt
import time
import requests
# sys.path.insert(1, os.path.dirname(__file__) + '/..')
user_home_path = str(Path.home())
os.makedirs(f'{user_home_path}/tweq-analizer/data_center/',exist_ok=True)
data_center = f'{user_home_path}/tweq-analizer/data_center/'

link = 'https://quality.data.gov.tw/dq_download_json.php?nid=11549&md5_url=bb878d47ffbe7b83bfc1b41d0b24946e'
data_request = requests.get(link)
row_data = pd.DataFrame(data_request .json())  #num of all stock
print(row_data)

row_data  = row_data .rename(columns={'證券代號':'STOCK_ID', '證券名稱':'NAME','成交股數':'V','成交金額':'T','開盤價':'O','最高價':'H','最低價':'L','收盤價':'C','漲跌價差':'D','成交筆數':'v'})
print(row_data )
historical_data = pd.DataFrame()
for i in row_data.index:    
    stock_id = row_data.loc[i, 'STOCK_ID'] + '.TW'
    data = yf.Ticker(stock_id)
    df = data.history(period="max")
    print(df)
    df.to_csv(f'{data_center}{stock_id}.csv')

    