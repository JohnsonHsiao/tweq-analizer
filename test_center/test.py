import pandas as pd
import statsmodels.api as sm
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import sys
from pathlib import Path
import os
user_home_path = str(Path.home())
data_center = f'{user_home_path}/tweq-analizer/data_center/'
fama_data = f'{user_home_path}/tweq-analizer/data_center/fama_data/'

fx_rate = pd.read_csv('/Users/johnsonhsiao/tweq-analizer/data_center/USD_TWD Historical Data.csv')
fx_rate = fx_rate.iloc[::-1]
fx_rate = fx_rate.reset_index(drop=True)

for stock in os.listdir(fama_data):
    stock = pd.read_csv(f'{fama_data}{stock}').drop(columns=["Unnamed: 0"])
    variable_table = pd.DataFrame(index = stock.index)
    variable_table['Date'] = stock['Date']
    variable_table['Individual Return'] = stock['Daily_Return']
    variable_table['Weighted Return'] = stock['market']
    variable_table['FX Factor'] = fx_rate['Price']
    variable_table['risk-free'] = stock['rf']
    variable_table['mkt-rf'] = stock['mkt-rf']
    variable_table['risk premium'] = variable_table['Individual Return'] - variable_table['risk-free']
    X = variable_table[['mkt-rf', 'FX Factor']]
    y = variable_table['risk premium']
    X = sm.add_constant(X)
    fx_model = sm.OLS(y, X).fit()
    print(fx_model.summary())
    intercept, b1, b2 = fx_model.params
    print(intercept, b1, b2)