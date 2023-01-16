import pandas as pd
from datetime import date, timedelta
import statsmodels.api as sm
import sys
from pathlib import Path
import os
user_home_path = str(Path.home())
data_center = f'{user_home_path}/tweq-analizer/data_center/'
stock_file = f'{user_home_path}/tweq-analizer/data_center/stock_data/'
os.makedirs(f'{user_home_path}/tweq-analizer/data_center/final_data', exist_ok=True)
final_data = f'{user_home_path}/tweq-analizer/data_center/final_data/'

df1 = pd.read_csv(f'{data_center}ff_table.csv')
ff_table = df1.dropna().reset_index(drop=True)
ff_table['rf'] = ff_table['rf']*0.01
stock_list = os.listdir(stock_file)

def final_table(ff_table, stock_list):
    for stock in stock_list:
        print(stock)
        stock_data = pd.read_csv(f'{stock_file}{stock}')
        stock_data.dropna().reset_index(drop=True)
        stock_data['Daily_Return'] = stock_data['Adj Close'].pct_change().dropna()
        joint = ff_table.merge(stock_data,on = ['Date'], how = 'left')
        joint['mkt-rf'] = joint['market'] - joint['rf']
        joint = joint.drop(index = 0)

        coefficient = []
        for i in range(0,836,1):
            coefficient.append(factor(i,joint))
        c_table = pd.DataFrame(coefficient, columns = ['const ','mkt-rf','SMB','HML'])
        c_table.index = c_table.index + 1

        expected_daily_return = []
        for i in range(11,837,1):
            a = er(i,joint,c_table)
            expected_daily_return.append(a)
            df4 = pd.DataFrame (expected_daily_return, columns = ['ER'])
            df4.index = df4.index + 1

        final = joint.drop(index = joint.index[0:129])
        final.index = final.index - 129
        final['abnormal_returns'] = df4['ER'] - final['Daily_Return']
        final.to_csv(f'{final_data}{stock}')

def factor(t,joint):
    X = joint[['mkt-rf', 'SMB', 'HML']].head(t+120)
    y = joint['Daily_Return'].head(t+120) - joint['rf'].head(t+120)
    X = sm.add_constant(X)
    ff_model = sm.OLS(y, X).fit()
    # print(ff_model.summary())
    intercept, b1, b2, b3 = ff_model.params
    c = [intercept, b1, b2, b3]
    return c

def rf(t,joint):
    return joint['rf'].loc[t]
def market_premium(t,joint):
    return joint['mkt-rf'].loc[t]
def size_premium(t,joint):
    return joint['SMB'].loc[t]
def value_premium(t,joint):
    return joint['HML'].loc[t]
def get_const(t,c_table):
    return c_table['const'].loc[t]
def get_mkt(t,c_table):
    return c_table['mkt-rf'].loc[t]
def get_SMB(t,c_table):
    return c_table['SMB'].loc[t]
def get_HML(t,c_table):
    return c_table['HML'].loc[t]
def er(t,joint,c_table):
    return rf(t-10,joint) + get_mkt(t-10,c_table) * market_premium(t-10,joint) + get_SMB(t-10,c_table) * size_premium(t-10,joint) + get_HML(t-10,c_table) * value_premium(t-10,joint)

if __name__ == '__main__':
    final_table(ff_table, stock_list) 