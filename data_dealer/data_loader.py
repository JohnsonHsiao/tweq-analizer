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
import tqdm

user_home_path = str(Path.home())
os.makedirs(f'{user_home_path}/tweq-analizer/data_center/', exist_ok=True)
data_center = f'{user_home_path}/tweq-analizer/data_center/'

capital_rank = pd.read_csv(f'{data_center}StockList.csv', names=['rank', 'id', 'pct'])
BPratio_rank = pd.read_csv(f'{data_center}BWIBBU_d_ALL_20221202.csv')
BPratio_rank = BPratio_rank.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1)
data = pd.merge(capital_rank, BPratio_rank, how='left', on=['id'])

def get_factor(data):
    big = data[:15]
    small = data[16:]
    sh = small[(small['bp'] > small['bp'].quantile(0.7))]
    sm = small[small['bp'].quantile(0.7) > (
        small['bp'] > small['bp'].quantile(0.3))]
    sl = small[(small['bp'] < small['bp'].quantile(0.3))]
    bh = big[(big['bp'] > big['bp'].quantile(0.7))]
    bm = big[big['bp'].quantile(0.7) > (big['bp'] > big['bp'].quantile(0.3))]
    bl = big[(big['bp'] < big['bp'].quantile(0.3))]
    return sh, sm, sl, bh, bm, bl

def get_stock_return(name):
    stock_return = ['Null']
    stock_data = yf.download(str(name)+'.TW', start ='2020-01-01')
    for num in range(len(stock_data)):
        if num+2 <= len(stock_data):
            stock_return.append((stock_data['Close'][num+1] - stock_data['Close'][num])/stock_data['Close'][num])
    stock_data['return'] = stock_return # market return
    return stock_data

def SMB_and_HML():
    temp = {}
    factor_list = ['SH','SM','SL','BH','BM','BL']
    for factor in get_factor(data):
        i = 0
        for index in tqdm(factor.index):
            stock_data = get_stock_return(factor['id'][index])
            stock_data = stock_data[stock_data['return']!='Null']
            print(stock_data)
            pct, _ = factor['pct'][index].split('%')
            print((stock_data['return'] * float(pct)))
            # temp[factor_list[i]]
        i += 1
    # SMB = (temp['SH'] + temp['SM'] + temp['SL'])/3 - (temp['BH'] + temp['BM'] + temp['BL'])/3
    # HML = (temp['SH'] + temp['BH'])/2 - (temp['SL'] + temp['BL'])/2
    # print(SMB, HML)


def ff_data_table():
    daily_data = yf.download('^TWII', start ='2020-01-01')
    daily_return = ['Null']
    for num in range(len(daily_data)):
        if num+2 <= len(daily_data):
            daily_return.append((daily_data['Close'][num+1] - daily_data['Close'][num])/daily_data['Close'][num])
    daily_data['return'] = daily_return # market return
    
if __name__ == '__main__':
    SMB_and_HML()

 