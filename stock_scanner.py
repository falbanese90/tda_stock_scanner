import pickle as pkl
import requests
from config import ameritrade
import pandas as pd
import time
import re
import os


def cleanTickers(energy_tickers):
    tickers = []
    for n in energy_tickers:
        if len(n) <= 4:
            tickers.append(n)
    return tickers
            

def retrieve_tickers(file):
    energy_bucket = pd.read_csv(file)
    energy_bucket = energy_bucket['Symbol']
    energy_tickers = []
    for n in energy_bucket:
        energy_tickers.append(n)
    tickers = cleanTickers(energy_tickers)
    return tickers

tickers = retrieve_tickers('energy_bucket.csv')


url = 'https://api.tdameritrade.com/v1/instruments'
start = 0
end = 50
files = []
while start < len(tickers):
    symbols = tickers[start:end]
    payload = {'apikey': ameritrade,
               'symbol': symbols,
               'projection': 'fundamental'}
    result = requests.get(url, params=payload)
    data = result.json()
    f_name = time.asctime() + '.pkl'
    f_name = re.sub(":", "_", f_name)
    f_name = re.sub(" ", "_", f_name)
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
    points = ['symbol', 'peRatio', 'pegRatio', 'high52']
    for ticker in tickers:
        tick = []
        for point in points:
            tick.append(info[ticker]['fundamental'][point])
        data.append(tick)
    os.remove(file)


    
    





    

    
    