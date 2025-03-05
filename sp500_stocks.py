import pandas as pd
import datetime
import numpy as np
import yfinance as yf
import pandas_ta


def loadData():
    sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    sp500['Symbol'] = sp500['Symbol'].str.replace('.', '-')
    symbols = sp500['Symbol'].unique().tolist()
    symbols.sort()
    symbols = symbols[:5]
    end_date = '2025-02-21'
    start_date = pd.to_datetime(end_date) - pd.DateOffset(365*5)
    df = yf.download(tickers=symbols,  interval="1d",start=start_date, end=end_date)
    df = df.stack()
    df.columns = df.columns.str.lower()
    df.to_pickle('D:/Development/finance/sp500_data.pkl')
    #df.to_json('D:/Development/finance/sp500_json.json')
    #df.to_csv('D:/Development/finance/sp500.csv')

def loadFromLocal():
    df = pd.read_pickle('D:/Development/finance/sp500_data.pkl')
    # Garman Klass Volatility
    df['Garman_Klass_vol'] = (np.log(df['high']) - np.log(df['low']))**2 - (2*np.log(2) - 1)*((np.log(df['close']) - np.log(df['open']))**2)

    df['RSI'] = df.groupby(level=1)['close'].transform(lambda x: pandas_ta.rsi(close = x, length = 20))
    closeSeries = df['close']
    a = pandas_ta.rsi(closeSeries, length = 20)
    print(df)
#loadData()
loadFromLocal()