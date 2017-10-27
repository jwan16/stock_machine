import bs4 as bs
import urllib.request
from stock.models import Historical_Price, Company
import datetime
import requests
import pandas as pd
import re
from socket import error as SocketError
import errno


# print(ratio)
# ratio.save()

stock_list = [i.stock_id for i in Company.objects.distinct()]


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
    period1 = datetime.datetime.strptime(start_date + '-8', '%Y-%m-%d-%H').strftime('%s')
    period2 = datetime.datetime.strptime(end_date + '-8', '%Y-%m-%d-%H').strftime('%s')
    url = 'https://query1.finance.yahoo.com/v7/finance/download/' + stock_id + '.HK?period1=' + str(
        period1) + '&period2=' + str(period2) + '&interval=1d&events=history&crumb=tgIGmTK3EA.'
    data = requests.get((url), headers=headers).text
    data2 = data.split('\n')
    for a in data2:
        price_list.append(a.split(','))
    df = pd.DataFrame(price_list, columns=price_list[0])
    df = df[1:]
    df['Date'] = pd.to_datetime(pd.Series(df['Date']))

    # Indexing Date
    df.index = df['Date']
    df.drop('Date', axis=1, inplace=True)

    df = df[df.notnull()].dropna()
    print(df)
    df = df[df['Volume'] != '0']
    for i in df.columns.values:
        df[i] = df[i].notnull()
        df[i] = df[i].astype(float)
    df = df.sort_index(ascending=True)

    return df

for i in stock_list:
    print(i)
    if int(i) < 10: stock_id = '000' + str(i)
    elif int(i) < 100: stock_id = '00' + str(i)
    elif int(i) < 1000: stock_id = '0' + str(i)
    listing_date = Company.objects.get(stock_id = i).listing_date.strftime('%Y-%m-%d')
    df = get_historical_price(stock_id, listing_date, '2017-10-20', 'daily')
    print(df)
    for a in range(0, df['Open'].count()):
        Historical_Price.objects.get_or_create(stock_id = Company.objects.get(stock_id=i), date = df.index[a])
        price = Historical_Price.objects.filter(stock_id = Company.objects.get(stock_id=i), date = df.index[a])
        # ratio = Ratio.objects.filter(RAT_COM_StockCode = code, RAT_Year = stock_list[i]['RAT_Year'][a])
        try: price.update(open = df['Open'][a])
        except: continue
        try: price.update(low = df['Low'][a])
        except: continue
        try: price.update(close = df['Close'][a])
        except: continue
        try: price.update(adj_close = df['Adj Close'][a])
        except: continue
        try: price.update(volume = df['Volume'][a])
        except: continue
