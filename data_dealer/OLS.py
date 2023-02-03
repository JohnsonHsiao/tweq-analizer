import pandas as pd
import numpy as np
import statsmodels.api as sm
import os

feature_data_file = '/Users/johnsonhsiao/Library/CloudStorage/OneDrive-個人/OLSdata'

def car(t):
    return (variable_table['Abnormal_Return'].loc[t+1]+variable_table['Abnormal_Return'].loc[t+2]+variable_table['Abnormal_Return'].loc[t+3])
    car(0)


for company in os.listdir(feature_data_file):
    if company != '.DS_Store': 
        print(company)
        stock_info = pd.read_excel(feature_data_file + '/' + company)
        stock_info.rename(columns = {'年月':'Date','TEJ產業_名稱':'Industry','應收帳款週轉次數':'Receivable Turnover Ratio','負債比率':'Debt Ratio','單月營收(千元)':'Revenue(k/per Month)','ROA(A)稅後息前':'ROA(Pre-tax)','ROE(A)－稅後':'ROE(After-tax)','公司年資':'Age'}, inplace = True)
        stock_info['Date']= stock_info['Date'].astype('datetime64')
        id = company.replace('.xlsx','')
        his_price = pd.read_csv(f'/Users/johnsonhsiao/Library/CloudStorage/OneDrive-個人/stock_data/{id}.TW.csv')
        his_price['Date']=his_price['Date'].astype('datetime64')
        combined = pd.merge(stock_info,his_price, how = "right", on = ["Date"])
        combined['Daily_Return'] = combined['Adj Close'].pct_change().dropna()
        combined = combined.drop(index = 0)
        df1 = pd.read_csv('/Users/johnsonhsiao/tweq-analizer/data_center/ff_table.csv')
        df1['Date'] = pd.to_datetime(df1['Date'])
        ff_table = df1[(df1.Date.isin(combined.Date))]
        ff_table = ff_table.dropna().reset_index(drop=True)
        ff_table['rf'] = ff_table['rf'] * 0.01
        ff_table['mkt-rf'] = ff_table['market'] - ff_table['rf']
        joint = combined[(combined.Date.isin(ff_table.Date))]
        joint = joint.reset_index(drop = True)
        fama_data = pd.read_csv(f'/Users/johnsonhsiao/tweq-analizer/data_center/fama_data/{id}.TW.csv')
        variable_table = joint.drop(index = joint.index[0:129])
        variable_table.index = variable_table.index - 128
        variable_table['Abnormal_Return'] = fama_data['abnormal_returns']
        car_table = []
        for i in range(0,771,1):
            car_table.append(car(i))
        car_table = pd.DataFrame(car_table, columns = ['3-day-CAR'])
        car_table.index = car_table.index+1
        final = variable_table.copy()
        final.drop(final.tail(2).index,inplace = True)
        final['3-day-CAR'] = car_table['3-day-CAR']
        final = pd.merge(final,ff_table, on = 'Date', how = 'left')
        final.to_csv(f'/Users/johnsonhsiao/tweq-analizer/data_center/final/{id}_3car.csv')






