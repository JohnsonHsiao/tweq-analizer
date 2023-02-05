import yfinance as yf
import pandas as pd
daily_data = yf.download('^TWII', start ='2018-12-30')
daily_return = ['Null']
for num in range(len(daily_data)):
    if num+2 <= len(daily_data):
        daily_return.append((daily_data['Close'][num+1] - daily_data['Close'][num])/daily_data['Close'][num])
daily_data['return'] = daily_return # market return
daily_data = daily_data[daily_data['return']!='Null']  #market return
daily_data.index = pd.to_datetime(daily_data.index).tz_localize(None) 
print(daily_data)