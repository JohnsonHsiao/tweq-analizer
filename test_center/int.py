import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

fama_table = pd.read_csv('/Users/johnsonhsiao/tweq-analizer/data_center/fama_data/1101.TW.csv').drop(columns=["Unnamed: 0"])


def car(date, t): 
    value = 0
    #(date, date+t+1, 1) loc[i]
    for i in range(-t, t+1, 1):
        value += fama_table['abnormal_returns'].loc[date+i]
    return value

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

car_table = []
for i in range(4,834,1):
    car_table.append(car(i,3))
car_table = pd.DataFrame(car_table, columns = ['t-3 CAR'])
car_table.index = car_table.index + 4
print(car_table)