import time
import pandas as pd
import numpy as np
import sys
from pathlib import Path
import os
user_home_path = str(Path.home())
data_center = f'{user_home_path}/tweq-analizer/data_center/'
stock_file = f'{user_home_path}/tweq-analizer/data_center/stock_data/'
fama_data = f'{user_home_path}/tweq-analizer/data_center/fama_data/'
os.makedirs(f'{user_home_path}/tweq-analizer/data_center/car_table', exist_ok=True)

def car_table():
    for stock in os.listdir(fama_data):
        fama_table = pd.read_csv(fama_data+stock).drop(columns=["Unnamed: 0"])
        print(fama_table)
        negative_one_to_t(fama_table)
        negative_two_to_t(fama_table)
        negative_three_to_t(fama_table)
        negative_three_to_positive_one(fama_table)
        negative_three_to_positive_two(fama_table)
        negative_three_to_positive_three(fama_table)
        fama_table.to_csv(f'{user_home_path}/tweq-analizer/data_center/car_table/{stock}')
        time.sleep(1.5)

def car(date, t, fama_table): 
    value = 0
    #(date, date+t+1, 1) loc[i]
    for i in range(date, date+t, 1):
        value += fama_table['abnormal_returns'].loc[i]
    return value

def negative_one_to_t(fama_table):
    car_table = []
    for i in range(0,836,1):
        car_table.append(car(i,2,fama_table))
    car_table = pd.DataFrame(car_table, columns = ['t-1~t CAR'])
    car_table.index = car_table.index + 1
    fama_table['t-1~t CAR'] = car_table['t-1~t CAR']
    print(fama_table)

def negative_two_to_t(fama_table):
    car_table = []
    for i in range(0,835,1):
        car_table.append(car(i,3,fama_table))
    car_table = pd.DataFrame(car_table, columns = ['t-2~t CAR'])
    car_table.index = car_table.index + 2
    fama_table['t-2~t CAR'] = car_table['t-2~t CAR']
    print(fama_table)
    
def negative_three_to_t(fama_table):
    car_table = []
    for i in range(0,834,1):
        car_table.append(car(i,4,fama_table))
    car_table = pd.DataFrame(car_table, columns = ['t-3~t CAR'])
    car_table.index = car_table.index + 3
    fama_table['t-3~t CAR'] = car_table['t-3~t CAR']
    print(fama_table)

def negative_three_to_positive_one(fama_table):
    car_table = []
    for i in range(0,833,1):
        car_table.append(car(i,5,fama_table))
    car_table = pd.DataFrame(car_table, columns = ['t-3~t+1 CAR'])
    car_table.index = car_table.index + 3
    fama_table['t-3~t+1 CAR'] = car_table['t-3~t+1 CAR']
    print(fama_table)

def negative_three_to_positive_two(fama_table):
    car_table = []
    for i in range(0,832,1):
        car_table.append(car(i,6,fama_table))
    car_table = pd.DataFrame(car_table, columns = ['t-3~t+2 CAR'])
    car_table.index = car_table.index + 3
    fama_table['t-3~t+2 CAR'] = car_table['t-3~t+2 CAR']
    print(fama_table)

def negative_three_to_positive_three(fama_table):
    car_table = []
    for i in range(0,831,1):
        car_table.append(car(i,7,fama_table))
    car_table = pd.DataFrame(car_table, columns = ['t-3~t+3 CAR'])
    car_table.index = car_table.index + 3
    fama_table['t-3~t+3 CAR'] = car_table['t-3~t+3 CAR']
    print(fama_table)

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

car_table()