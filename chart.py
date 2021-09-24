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
        n['datetime'] = str(pd.to_datetime(n['datetime'], unit='ms'))

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


