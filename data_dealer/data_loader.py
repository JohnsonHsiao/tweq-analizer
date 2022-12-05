from operator import index
import yfinance as yf
import requests
import numpy as np
import pandas as pd
import json
import sys
from pathlib import Path
import os
from datetime import datetime, timedelta
import time
import requests

user_home_path = str(Path.home())
os.makedirs(f'{user_home_path}/tweq-analizer/data_center/', exist_ok=True)
data_center = f'{user_home_path}/tweq-analizer/data_center/'

capital_rank = pd.read_csv(
    '/Users/johnsonhsiao/tweq-analizer/data_center/StockList.csv', names=['rank', 'id', 'pct'])
BPratio_rank = pd.read_csv(
    '/Users/johnsonhsiao/tweq-analizer/data_center/BWIBBU_d_ALL_20221202.csv')
BPratio_rank = BPratio_rank.drop(
    ['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1)
data = pd.merge(capital_rank, BPratio_rank, how='left', on=['id'])


def get_factor(data):
    big = data[:15]
    small = data[16:]
    SH = small[(small['bp'] > small['bp'].quantile(0.7))]
    SM = small[small['bp'].quantile(0.7) > (
        small['bp'] > small['bp'].quantile(0.3))]
    SL = small[(small['bp'] < small['bp'].quantile(0.3))]
    BH = big[(big['bp'] > big['bp'].quantile(0.7))]
    BM = big[big['bp'].quantile(0.7) > (big['bp'] > big['bp'].quantile(0.3))]
    BL = big[(big['bp'] < big['bp'].quantile(0.3))]
    return SH, SM, SL, BH, BM, BL


def get_daily_data(name):
    daily_data = yf.download(
        str(name)+'.TW', start_date = '2020-01-01')
    daily_data['roi'] = (daily_data['close'] -
        daily_data['open']) / daily_data['open']
    print(daily_data)
        
if __name__ == '__main__':
    get_daily_data(data)
 