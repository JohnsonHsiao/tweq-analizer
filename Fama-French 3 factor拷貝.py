#!/usr/bin/env python
# coding: utf-8

# In[1]:


from yahoo_fin.stock_info import *
import pandas as pd
from datetime import date, timedelta
import statsmodels.api as sm
import getFamaFrenchFactors as gff
symbol = '2330.tw'
df = get_data(symbol, start_date = datetime.datetime.now() - datetime.timedelta(365))
df


# In[2]:


df = df.reset_index(level=0)
df


# In[3]:


df.rename(columns={df.columns[0]: 'Date'},inplace=True)
df


# In[4]:


ff3_monthly = gff.famaFrench3Factor(frequency='m')
ff3_monthly.rename(columns={"date_ff_factors": 'Date'}, inplace=True)
ff3_monthly.set_index('Date', inplace=True)


# In[5]:


df.index = pd.to_datetime(df.Date)
df


# In[6]:


stock_returns = df['adjclose'].resample('M').last().pct_change().dropna()
stock_returns.name = "Month_Rtn"


# In[7]:


ff_data = ff3_monthly.merge(stock_returns,on='Date')
ff_data


# In[8]:


X = ff_data[['Mkt-RF', 'SMB', 'HML']]
y = ff_data['Month_Rtn'] - ff_data['RF']
X = sm.add_constant(X)
ff_model = sm.OLS(y, X).fit()
print(ff_model.summary())
intercept, b1, b2, b3 = ff_model.params


# In[9]:


rf = ff_data['RF'].mean()
market_premium = ff3_monthly['Mkt-RF'].mean()
size_premium = ff3_monthly['SMB'].mean()
value_premium = ff3_monthly['HML'].mean()


# In[10]:


expected_monthly_return = rf + b1 * market_premium + b2 * size_premium + b3 * value_premium 
expected_yearly_return = expected_monthly_return * 12
print("Expected yearly return: " + str(expected_yearly_return))


# In[11]:


expected_daily_return = expected_monthly_return / 30
print(expected_daily_return)


# In[12]:


df['daily_returns']=(df['close'].pct_change())
df


# In[13]:


df['abnormal_returns'] = expected_daily_return - df['daily_returns']
df

