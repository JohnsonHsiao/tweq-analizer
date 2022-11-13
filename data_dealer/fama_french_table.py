from yahoo_fin.stock_info import *
import pandas as pd
from datetime import date, timedelta
import statsmodels.api as sm
import getFamaFrenchFactors as gff
from data_loader import get_stock_id
import logging
logging.basicConfig(filename='./tweq-analizer/data_center/loader_server.log', level=logging.INFO)

logger = logging.getLogger(__name__)

def get_ffdata(symbol): # Mkt-RF,SMB,HML,RF,Month_Rtn by month
    
    symbol = f'{symbol}.TW'
    data = get_data(symbol, start_date = datetime.datetime.now() - datetime.timedelta(900))
    data = data.reset_index(level=0)
    data.rename(columns={data.columns[0]: 'Date'},inplace=True)
    ff3_monthly = gff.famaFrench3Factor(frequency='m')
    ff3_monthly.rename(columns={"date_ff_factors": 'Date'}, inplace=True)
    ff3_monthly.set_index('Date', inplace=True)
    data.index = pd.to_datetime(data.Date)
    stock_returns = data['adjclose'].resample('M').last().pct_change().dropna()
    stock_returns.name = "Month_Rtn"
    ff_data = ff3_monthly.merge(stock_returns,on='Date')  # Mkt-RF,SMB,HML,RF,Month_Rtn by month
    return ff_data, ff3_monthly, data

def create_table(symbol): 

    ff_data, ff3_monthly, data = get_ffdata(symbol)
    X = ff_data[['Mkt-RF', 'SMB', 'HML']]
    y = ff_data['Month_Rtn'] - ff_data['RF']
    X = sm.add_constant(X)
    ff_model = sm.OLS(y, X).fit()
    # print(ff_model.summary())
    logging.info(ff_model.summary())
    intercept, b1, b2, b3 = ff_model.params #const  Mkt-RF SMB  HML 
    rf = ff_data['RF'].mean()
    market_premium = ff3_monthly['Mkt-RF'].mean()
    size_premium = ff3_monthly['SMB'].mean()
    value_premium = ff3_monthly['HML'].mean()

    expected_monthly_return = rf + b1 * market_premium + b2 * size_premium + b3 * value_premium 
    expected_yearly_return = expected_monthly_return * 12
    print("Expected yearly return: " + str(expected_yearly_return))

    expected_daily_return = expected_monthly_return / 30
    print(expected_daily_return)

    data['daily_returns']=(data['close'].pct_change())
    data['abnormal_returns'] = expected_daily_return - data['daily_returns']
    logging.info(data)
    result = data[['ticker','daily_returns','abnormal_returns']]
    print(result)

if __name__ == '__main__':
    for name in get_stock_id():
        create_table(name)