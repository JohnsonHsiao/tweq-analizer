import pandas as pd
import statsmodels.api as sm
import numpy as np
import yfinance as yf
import sys
from pathlib import Path
import os
import time

user_home_path = str(Path.home())
data_center = f'{user_home_path}/tweq-analizer/data_center/'
fama_data = f'{user_home_path}/tweq-analizer/data_center/fama_data/'
os.makedirs(f'{user_home_path}/tweq-analizer/data_center/fx_table', exist_ok=True)
fx_table = f'{data_center}fx_table/'
def ols(df):
    X = df[['mkt-rf', 'FX Factor']]
    y = df['risk premium']
    X = sm.add_constant(X)
    fx_model = sm.OLS(y, X).fit()
    # print(fx_model.summary())
    intercept, b1, b2 = fx_model.params
    # print(intercept)
    df['const'] = intercept
    df['[mkt-rf]'] = b1
    df['FX factor'] = b2
    summary_df = pd.read_html(fx_model.summary().tables[1].as_html(), header=0, index_col=0)[0]    
    return df, summary_df

for id in os.listdir('/Users/johnsonhsiao/Library/CloudStorage/OneDrive-個人/tweq-analyzer/stock_data'):
    name = id.split('.')[0]
    if os.path.isfile(os.path.join(f'{fx_table}{name}',f'{fx_table}{name}/{id}')):
        print(name)
    else:
        stock = pd.read_csv(f'/Users/johnsonhsiao/Library/CloudStorage/OneDrive-個人/tweq-analyzer/stock_data/{id}')
        stock['Date'] = pd.to_datetime(stock['Date']).dt.date
        twii = yf.download('^TWII', start = '2019-01-01', end = '2022-12-31').reset_index()
        # print(twii)
        twii['Date'] = pd.to_datetime(twii['Date']).dt.date
        twii['Daily Return'] = twii['Adj Close'].pct_change().dropna()
        stock['mkt'] = twii['Daily Return']
        rf = pd.read_csv('/Users/johnsonhsiao/tweq-analizer/data_center/Taiwan 10-Year Bond Yield Historical Data.csv')
        rf['Date'] = pd.to_datetime(rf['Date']).dt.date
        stock = pd.merge(stock, rf[['Date', 'Price']], on='Date', how='left')
        fx_rate = pd.read_csv('/Users/johnsonhsiao/tweq-analizer/data_center/USD_TWD Historical Data.csv')
        fx_rate['Date'] = pd.to_datetime(fx_rate['Date']).dt.date
        # print(fx_rate)
        stock = pd.merge(stock, fx_rate[['Date', 'Price']], on='Date', how='left',suffixes=('', '_fx'))
        stock = stock.rename(columns={'Price': 'rf', 'Price_fx': 'fx_price'})
        stock = stock.dropna()
        stock['return'] = stock['return'].astype(float)
        
        print(id)

        variable_table = pd.DataFrame(index = stock.index)
        variable_table['Date'] = stock['Date']
        variable_table['Individual Return'] = stock['return'].dropna()
        variable_table['Weighted Return'] = stock['mkt']
        variable_table['FX Factor'] = stock['fx_price']
        variable_table['risk-free'] = stock['rf']
        variable_table['mkt-rf'] = variable_table['Weighted Return'] - variable_table['risk-free']
        variable_table['risk premium'] = variable_table['Individual Return'] - variable_table['risk-free']
        df1 , first = ols(variable_table[:233])
        df2 , second = ols(variable_table[233:478])
        df3 , third = ols(variable_table[478:721])
        df4 , forth = ols(variable_table[721:])

        result = pd.concat([df1,df2,df3,df4])
        
        os.makedirs(f'{fx_table}{name}', exist_ok=True)
        first.to_csv(f'{fx_table}{name}/first.csv')
        second.to_csv(f'{fx_table}{name}/second.csv')
        third.to_csv(f'{fx_table}{name}/third.csv')
        forth.to_csv(f'{fx_table}{name}/forth.csv')
        result.to_csv(f'{fx_table}{name}/{id}')


