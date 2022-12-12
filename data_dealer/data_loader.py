from operator import index
import yfinance as yf
import requests
import numpy as np
import pandas as pd
from  datetime import datetime
import json
import sys
from pathlib import Path
import os
import time
import requests

user_home_path = str(Path.home())
os.makedirs(f'{user_home_path}/tweq-analizer/data_center/', exist_ok=True)
os.makedirs(f'{user_home_path}/tweq-analizer/data_center/stock_data', exist_ok=True)
data_center = f'{user_home_path}/tweq-analizer/data_center/'
stock_file = f'{user_home_path}/tweq-analizer/data_center/stock_data/'

capital_rank = pd.read_csv(f'{data_center}StockList.csv', names=['rank', 'id', 'pct'])
BPratio_rank = pd.read_csv(f'{data_center}BWIBBU_d_ALL_20221202.csv')
BPratio_rank = BPratio_rank.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1)
data = pd.merge(capital_rank, BPratio_rank, how='left', on=['id'])
rf = pd.read_csv(f'{data_center}Taiwan 10-Year Bond Yield Historical Data.csv')
rf['Date'] = pd.to_datetime(rf['Date'])
rf.set_index('Date', inplace = True)
rf = rf.reindex(index=rf.index[::-1])

def get_factor(data):
    big = data[:15]
    small = data[16:]
    sh = small[(small['bp'] > small['bp'].quantile(0.7))]
    sm = small[((small['bp'].quantile(0.7) > small['bp']) & (small['bp'] > small['bp'].quantile(0.3)))]
    sl = small[(small['bp'] < small['bp'].quantile(0.3))]
    bh = big[(big['bp'] > big['bp'].quantile(0.7))]
    bm = big[((big['bp'].quantile(0.7) > big['bp']) & (big['bp'] > big['bp'].quantile(0.3)))]
    bl = big[(big['bp'] < big['bp'].quantile(0.3))]
    return bh, bm, bl, sh, sm, sl

def get_stock_return(name):
    stock_return = ['Null']
    stock_data = yf.download(str(name)+'.TW', start ='2019-12-30')
    for num in range(len(stock_data)):
        if num+2 <= len(stock_data):
            stock_return.append((stock_data['Close'][num+1] - stock_data['Close'][num])/stock_data['Close'][num])
    stock_data['return'] = stock_return # stock return
    stock_data.to_csv(f'{stock_file}{name}.TW.csv')
    return stock_data

def SMB_and_HML():
    temp = {}
    factor_list = ['BH','BM','BL','SH','SM','SL']
    i = 0
    a = 0
    for factor in get_factor(data):
        temp_list = []
        for index in factor.index:
            stock_data = get_stock_return(factor['id'][index])
            stock_data = stock_data[stock_data['return']!='Null']
            # print(stock_data)
            pct, _ = factor['pct'][index].split('%')
            stock_return = stock_data['return'] * float(pct)
            temp_list.append(stock_return)
            print(a)
            a += 1
        temp[factor_list[i]] = pd.DataFrame(temp_list).sum()
        i += 1
        # print(temp)
    SMB =  (temp['SH'] + temp['SM'] + temp['SL'])/3 -(temp['BH'] + temp['BM'] + temp['BL'])/3 
    HML = (temp['SH'] + temp['BH'])/2 - (temp['SL'] + temp['BL'])/2
    return SMB, HML
    

def ff_data_table():
    daily_data = yf.download('^TWII', start ='2019-12-30')
    daily_return = ['Null']
    for num in range(len(daily_data)):
        if num+2 <= len(daily_data):
            daily_return.append((daily_data['Close'][num+1] - daily_data['Close'][num])/daily_data['Close'][num])
    daily_data['return'] = daily_return # market return
    daily_data = daily_data[daily_data['return']!='Null']  #market return
    SMB, HML = SMB_and_HML()
    ff_table = pd.concat([daily_data['return'], rf['Price'], SMB,HML], axis = 1)
    ff_table.columns = ['market', 'rf', 'SMB', 'HML']
    ff_table.to_csv(f'{data_center}ff_table.csv')
    
if __name__ == '__main__':
    ff_data_table()  