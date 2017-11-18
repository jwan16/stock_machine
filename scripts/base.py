
# coding: utf-8


import pandas as pd
import requests
import datetime
import matplotlib.pyplot as plt
import numpy as np
import time



def get_historical_price(stock_id, start_date, end_date, frequency):
    price_list = []
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; 125LA; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022)',
        'Connection': 'Keep-Alive',
        'Content-Type': 'text/plain; Charset=UTF-8',
        'Accept': '*/*',
        'Accept-Language': 'zh-cn',
        'Cookie': 'B=4aos411brv8q6&b=3&s=a7; PRF=t%3D0' + str(stock_id) + '.HK; bnpt=1501232783&pnid=&pnct=',
    }
    period1 = datetime.datetime.strptime(start_date+'-8', '%Y-%m-%d-%H').strftime('%s')
    period2 = datetime.datetime.strptime(end_date+'-8', '%Y-%m-%d-%H').strftime('%s')
    url = 'https://query1.finance.yahoo.com/v7/finance/download/' + stock_id + '.HK?period1=' + str(period1) + '&period2=' + str(period2) + '&interval=1d&events=history&crumb=tgIGmTK3EA.'
    data = requests.get((url),headers=headers).text
    data2 = data.split('\n')
    for a in data2:
        price_list.append(a.split(','))
    df = pd.DataFrame(price_list, columns = price_list[0])
    df = df[1:]
    df['Date'] = pd.to_datetime(pd.Series(df['Date']))
    
    # frequency operation
    if frequency is 'weekly':
        df = df.groupby([df.Date.dt.strftime('%Y'),df.Date.dt.strftime('%W')]).last()
    elif frequency is 'monthly':
        df = df.groupby(df.Date.dt.strftime('%Y-%m')).last()
    
    # Indexing Date
    df.index = df['Date']
    df.drop('Date', axis = 1, inplace = True)

    df = df[df.notnull()].dropna()
    df = df[df['Volume'] != '0']
    for i in df.columns.values:
        df[i] = df[i].astype(float)
    df = df.sort_index(ascending=True)
    
    return df

def get_ewm(stock_id, start_date, end_date, frequency, days):
    d = datetime.datetime.strptime(start_date, '%Y-%m-%d') - datetime.timedelta(days= 3 * days)
    d = d.strftime('%Y-%m-%d')
    df = get_historical_price(stock_id, d, end_date, frequency)
    sma = df['Close'].rolling(window=days, min_periods=days).mean()[:days]
    rest = df['Close'][days:]
    df['ewm'+str(days)] = pd.concat([sma, rest]).ewm(span=days, adjust=False).mean()
    
    # get data after start date
    df = df[df.index >= datetime.datetime.strptime(start_date, '%Y-%m-%d')]
    return df['ewm'+str(days)]

def get_macd(stock_id, start_date, end_date, frequency, days1, days2):
    d = datetime.datetime.strptime(start_date, '%Y-%m-%d') - datetime.timedelta(days= 30 * days2)
    d = d.strftime('%Y-%m-%d')
    df = get_historical_price(stock_id, d, end_date, frequency)
    ewm1 = get_ewm(stock_id, d, end_date, frequency, days1)
    ewm2 = get_ewm(stock_id, d, end_date, frequency, days2)
    df['macd'] = ewm1 - ewm2
    
    #EMA of macd
    sma = df['macd'].rolling(window=9, min_periods=9).mean()[:9]
    rest = df['macd'][9:]
    df['ema9'] = pd.concat([sma, rest]).ewm(span=9, adjust=False).mean()
    
    # get data after start date
    df = df[df.index >= datetime.datetime.strptime(start_date, '%Y-%m-%d')]
    return df[['macd', 'ema9']]

def get_rsi(stock_id, start_date, end_date, frequency, days):
    d = datetime.datetime.strptime(start_date, '%Y-%m-%d') - datetime.timedelta(days= 3 * days)
    d = d.strftime('%Y-%m-%d')
    df = get_historical_price(stock_id, d, end_date, frequency)

    close = df['Adj Close']
    delta = close.diff()
    delta = delta[1:] 

    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    # Calculate the EWMA
    roll_up1 = pd.stats.moments.ewma(up, days)
    roll_down1 = pd.stats.moments.ewma(down.abs(), days)

    # Calculate the RSI based on EWMA
    RS1 = roll_up1 / roll_down1
    df['rsi'+str(days)]= 100.0 - (100.0 / (1.0 + RS1))

    df = df[df.index >= datetime.datetime.strptime(start_date, '%Y-%m-%d')]
    return df['rsi'+str(days)]



def get_stochastic_k_fast(stock_id, start_date, end_date, frequency, days, period):
    d = datetime.datetime.strptime(start_date, '%Y-%m-%d') - datetime.timedelta(days= 30 * days)
    d = d.strftime('%Y-%m-%d')
    df = get_historical_price(stock_id, d, end_date, frequency)
    df['L' + str(days)] = pd.stats.moments.rolling_min(df['Low'], days)
    df['H' + str(days)] = pd.stats.moments.rolling_max(df['High'], days)
    df['k_fast'] = 100 * (df['Close'] - df['L'+str(days)]) / (df['H' + str(days)] - df['L' + str(days)])
    df = df[df.index >= datetime.datetime.strptime(start_date, '%Y-%m-%d')]
    return df['k_fast']

def get_stochastic_k_slow(stock_id, start_date, end_date, frequency, days, period):
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m-%d')
    d = datetime.datetime.strptime(start_date, '%Y-%m-%d') - datetime.timedelta(days= 30 * days)
    d = d.strftime('%Y-%m-%d')
    df = get_historical_price(stock_id, d, end_date, frequency)
    df['L' + str(days)] = pd.stats.moments.rolling_min(df['Low'], days)
    df['H' + str(days)] = pd.stats.moments.rolling_max(df['High'], days)
    df['k_fast'] = 100 * (df['Close'] - df['L'+str(days)]) / (df['H' + str(days)] - df['L' + str(days)])
    df['d_fast'] = pd.stats.moments.rolling_mean(df['k_fast'], period)
    df['k_slow'] = df['d_fast']
    df = df[df.index >= datetime.datetime.strptime(start_date, '%Y-%m-%d')]
    return df['k_slow']

def get_stochastic_d_slow(stock_id, start_date, end_date, frequency, days, period):
    d = datetime.datetime.strptime(start_date, '%Y-%m-%d') - datetime.timedelta(days= 30 * days)
    d = d.strftime('%Y-%m-%d')
    df = get_historical_price(stock_id, d, end_date, frequency)
    df['L' + str(days)] = pd.stats.moments.rolling_min(df['Low'], days)
    df['H' + str(days)] = pd.stats.moments.rolling_max(df['High'], days)
    df['k_fast'] = 100 * (df['Close'] - df['L'+str(days)]) / (df['H' + str(days)] - df['L' + str(days)])
    df['d_fast'] = pd.stats.moments.rolling_mean(df['k_fast'], period)
    df['k_slow'] = df['d_fast']
    df['d_slow'] = pd.stats.moments.rolling_mean(df['k_slow'], period)
    df = df[df.index >= datetime.datetime.strptime(start_date, '%Y-%m-%d')]
    return df['d_slow']

def get_bollinger_band(stock_id, start_date, end_date, frequency, days):
    d = datetime.datetime.strptime(start_date, '%Y-%m-%d') - datetime.timedelta(days= 3 * days)
    d = d.strftime('%Y-%m-%d')
    df = get_historical_price(stock_id, d, end_date, frequency)
    df['bb_ma'] = pd.stats.moments.rolling_mean(df['Adj Close'], days)
    df['sd'] = pd.stats.moments.rolling_std(df['Adj Close'], days)
    df['bb_upper'] = df['bb_ma'] + (df['sd']*2)
    df['bb_lower'] = df['bb_ma'] - (df['sd']*2)
    df = df[df.index >= datetime.datetime.strptime(start_date, '%Y-%m-%d')]
    return (df[['bb_upper', 'bb_ma', 'bb_lower']])

def get_moving_avg(stock_id, start_date, end_date, frequency, days):
    d = datetime.datetime.strptime(start_date, '%Y-%m-%d') - datetime.timedelta(days= 3 * days)
    d = d.strftime('%Y-%m-%d')
    df = get_historical_price(stock_id, d, end_date, frequency)
    df[str(days)+'ma'] = pd.stats.moments.rolling_mean(df['Close'], days)
    df.index = pd.to_datetime(df.index)
    df = df[df.index >= datetime.datetime.strptime(start_date, '%Y-%m-%d')]
    return df[str(days)+'ma']


# In[7]:

def plot_bollinger_band(df):
    df.plot(y=['Adj Close','ma', 'Upper Band', 'Lower Band'], title='Bollinger Bands')


# In[33]:


def macd_signal(stock_id, start_date, end_date, frequency):
    his_price = get_historical_price(stock_id, start_date, end_date, frequency)['Close']
    macd = get_macd(stock_id, start_date, end_date, frequency, 12, 26)
    df = pd.concat([his_price, macd], axis=1)
#     df[['macd_signal'] = (df['macd'] > df['ema9']) & (df['macd'] > 0)
#     df.loc[(df['macd']>0) & (df['macd'] > df['ema9']) & (df['macd'].shift(+1) < 0),'Signal'] = 'Strong buy'
    df.loc[(df['macd']>0) & (df['macd'] > df['ema9']) & (df['macd'].shift(+1) < df['ema9'].shift(+1)) ,'signal'] = 'Strong up'
#     df.loc[(df['macd']<0) & (df['macd'] > df['ema9']),'signal'] = 'Weak up'
#     df.loc[(df['macd']>0) & (df['macd'] < df['ema9']) ,'signal'] = 'Strong down'
#     df.loc[(df['macd']<0) & (df['macd'] < df['ema9']) ,'signal'] = 'Weak down'
    return df



# In[38]:

def macd_slope_change(stock_id, start_date, end_date, frequency):
    his_price = get_historical_price(stock_id, start_date, end_date, frequency)['Close']
    macd = get_macd(stock_id, start_date, end_date, frequency, 12, 26)
    df = pd.concat([his_price, macd], axis=1)
    df.loc[(df['macd'] > df['macd'].shift(+1)) & (df['macd'].shift(+1) < df['ema9'].shift(+1)) ,'signal'] = '-veto+ve'
    df.loc[(df['macd'] < df['macd'].shift(+1)) & (df['macd'].shift(+1) > df['ema9'].shift(+1)) ,'signal'] = '+veto-ve'
    return df

