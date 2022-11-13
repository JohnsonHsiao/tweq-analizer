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

user_home_path = str(Path.home())
os.makedirs(f'{user_home_path}/tweq-analizer/data_center/',exist_ok=True)
data_center = f'{user_home_path}/tweq-analizer/data_center/'

def get_stock_id():
    url = 'https://quality.data.gov.tw/dq_download_json.php?nid=11549&md5_url=bb878d47ffbe7b83bfc1b41d0b24946e'
    data_request = requests.get(url)
    row_data = pd.DataFrame(data_request .json())  #num of all stock
    row_data  = row_data .rename(columns={'證券代號':'STOCK_ID'})
    return row_data['STOCK_ID'] # 9958 
