import requests
import pandas as pd
import os
import csv
from datetime import datetime
import time
import matplotlib.pyplot as plt
from config import ameritrade, points
import pickle as pkl
import tools
from pprint import pprint
from models import Equity
import math
import numpy as np


def chart(ticker):
    ticker = ticker.upper()
    result = requests.get('https://api.tdameritrade.com/v1/instruments',
                          params={'apikey': ameritrade, 'symbol': ticker,
                          'projection': 'fundamental'})
    data = result.json()
    fd = data[ticker]['fundamental']

    result  = requests.get(f'https://api.tdameritrade.com/v1/marketdata/{ticker}/pricehistory', params={'apikey': ameritrade, 'periodType': 'year', 'frequencyType': 'daily'})
    data = result.json()
    for n in data['candles']:
        n['datetime'] = pd.to_datetime(n['datetime'], unit='ms').strftime('%m/%d/%Y')

    candles = data['candles']
    field = []
    for n in candles[0].keys():
        field.append(n)
    with open('price.csv', 'w') as outfile:
        fieldnames = field
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for n in candles:
            writer.writerow(n)
    time.sleep(5)

    df = pd.read_csv('price.csv')
    df = df.iloc[:, ::-1]
    df['MA10'] = df['close'].rolling(window=10).mean()
    df['MA20'] = df['close'].rolling(window=20).mean()
#    df['Log returns'] = np.log(df['close'] / data['close'].shift())
    x = 0
    l = []
    for n in df['close']:
        if x == 0:
            n = None
        else:
            n = np.log(n / df['close'][x - 1])
        x += 1
        l.append(n)
    df['Log returns'] = l
    
    df['HVSD30'] = df['Log returns'].rolling(30).std()
    list = []
    for n in df['HVSD30']:
        if n is None:
            result = None
        else:
            result = round((n * math.sqrt(252)) * 100, 3)
        list.append(result)
    df['HV'] = list
            
#     x = 0
#     list = []
#     for n in df['close']:
#         if x == 0:
#             result = None
#         else:
#             result = 100 * (abs(math.log(n / df['close'][x-1])))
#         list.append(result)
#         x += 1
#     df['Abs(R)'] = list
#     df['30dayHVSD'] = df['close'].rolling(30).std()
#     for n in df['30dayHVSD']:
#         if n is None:
#             pass
#         else:
#             offset = n
#     hv = []
#     for n in df['30dayHVSD']:
#         if n is None:
#             result = None
#         else:
#             result = round(n * math.sqrt(252), 2)
#         hv.append(result)
#     df['30dayHV'] = hv
    df.set_index('datetime', inplace=True)

    dict = {'chart': df, 'fundamental': fd}
    return dict


def fetch_analysis(file):
    tickers = tools.retrieve_tickers(file)
    start = 0
    end = 50
    files = []
    while start < len(tickers):
        symbols = tickers[start:end]
        payload = {'apikey': ameritrade,
                   'symbol': symbols,
                   'projection': 'fundamental'}
        result = requests.get('https://api.tdameritrade.com/v1/instruments', params=payload)
        data = result.json()
        f_name = tools.time_as_name('.pkl')
        files.append(f_name)
        with open(f_name, 'wb') as file:
            pkl.dump(data, file)
        start = end
        end += 50
        time.sleep(1)

    data = []
    for file in files:
        with open(file, 'rb') as f:
            info = pkl.load(f)
        tickers = list(info)

        for ticker in tickers:
            tick = list()
            for point in points:
                tick.append(info[ticker]['fundamental'][point])
                data.append(tick)
                os.remove(file)
    df = pd.DataFrame(data, columns=points)

    return df

def plot(dataframe, title):
    plt.figure(figsize=[16, 8])
    plt.plot(dataframe['close'], label=title)
    plt.plot(dataframe['MA10'], label='MA10')
    plt.plot(dataframe['MA20'], label='MA20')
    plt.ylabel('Price')
    plt.xlabel('Date')
    plt.legend()
    plt.savefig(f'{title}.png')
    ax = plt.gca()
    ax.axes.xaxis.set_ticks([])
    plt.grid(True)
    plt.show()


def options(ticker):
    ticker = ticker.upper()
    result = requests.get('https://api.tdameritrade.com/v1/marketdata/chains',
                          params={'apikey': ameritrade, 'symbol': ticker,
                          'contractType': 'CALL', 'strategy': 'ANALYTICAL', 'strikeCount': '1'})
    data = result.json()
    exp = [n for n in data['callExpDateMap'].keys()]
    strike = {}
    strike[f'{exp[4]}'] = data['callExpDateMap'][exp[4]]
    x = 0
    while x <= 1:
        for n in strike.keys():
            key = n
        strike = strike[key]
        x += 1
    return strike[0]

