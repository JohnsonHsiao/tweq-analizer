import pandas as pd
from datetime import date, timedelta
import statsmodels.api as sm
import sys
from pathlib import Path
import os
user_home_path = str(Path.home())
data_center = f'{user_home_path}/tweq-analizer/data_center/'
stock_file = f'{user_home_path}/tweq-analizer/data_center/stock_data/'
os.makedirs(f'{user_home_path}/tweq-analizer/data_center/fama_data', exist_ok=True)
fama_data = f'{user_home_path}/tweq-analizer/data_center/fama_data/'

df1 = pd.read_csv(f'{data_center}ff_table.csv', index_col = 'Date')
ff_table = df1.dropna()
ff_table['rf'] = ff_table['rf']*0.01
ff_table.index = ff_table.index.astype('datetime64')
stock_list = os.listdir(stock_file)

def final_table(ff_table, stock_list):
    for stock in stock_list:
        print(stock)
        stock_data = pd.read_csv(f'{stock_file}{stock}', index_col = 'Date')
        stock_data.dropna().reset_index(drop=True)
        stock_data['Daily_Return'] = stock_data['Adj Close'].pct_change().dropna()
        stock_data.index = pd.to_datetime(stock_data.index).tz_localize(None)
        joint = ff_table.join(stock_data)
        joint['mkt-rf'] = joint['market'] - joint['rf']
        print(joint)

        coefficient = []
        for i in range(0,847,1):
            coefficient.append(factor(i,joint))
        c_table = pd.DataFrame(coefficient, columns = ['const','(mkt-rf)','(SMB)','(HML)'])
        c_table.index = c_table.index + 1
        print(c_table)
        final = joint.drop(index = joint.index[0:130]).reset_index(0)
        expected_daily_return = []
        for i in range(11,848,1):
            a = er(i,joint,c_table)
            expected_daily_return.append(a)
            final['ER'] = pd.DataFrame (expected_daily_return)
        final['abnormal_returns'] = final['ER'] - final['Daily_Return']
        final = final.join(c_table)
        print(final)
        final.to_csv(f'{fama_data}{stock}')

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
    return joint['rf'].iloc[t]
def market_premium(t,joint):
    return joint['mkt-rf'].iloc[t]
def size_premium(t,joint):
    return joint['SMB'].iloc[t]
def value_premium(t,joint):
    return joint['HML'].iloc[t]
def get_const(t,c_table):
    return c_table['const'].iloc[t]
def get_mkt(t,c_table):
    return c_table['(mkt-rf)'].iloc[t]
def get_SMB(t,c_table):
    return c_table['(SMB)'].iloc[t]
def get_HML(t,c_table):
    return c_table['(HML)'].iloc[t]
def er(t,joint,c_table):
    return rf(t-10,joint) + get_mkt(t-10,c_table) * market_premium(t-10,joint) + get_SMB(t-10,c_table) * size_premium(t-10,joint) + get_HML(t-10,c_table) * value_premium(t-10,joint)

if __name__ == '__main__':
    final_table(ff_table, stock_list) 
