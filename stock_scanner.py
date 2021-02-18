import pickle as pkl
import requests
from config import ameritrade
import pandas as pd
import time
import re
import os


def retrieve_tickers(file):
    energy_bucket = pd.read_csv(file)
    energy_bucket = energy_bucket['Symbol']
    energy_tickers = []
    for n in energy_bucket:
        energy_tickers.append(n)
    tickers = cleanTickers(energy_tickers)
    return tickers


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


# creates a list with all instrument outputs
with open('instrument_list.pkl', 'rb') as col:
    columns = pkl.load(col)
# retieves tickers from selected bucket and cleans them
tickers = retrieve_tickers('tech_bucket.csv')

# breaks list into sections of 50 loads json into pkl files
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

# loads pkl files and creates a list with contents
data = []
for file in files:
    with open(file, 'rb') as f:
        info = pkl.load(f)
    tickers = list(info)
    # this is default, every output. Replace with list of
    # selected parameters from column list to refine
    points = ['symbol', 'peRatio', 'netProfitMarginTTM', 'vol1DayAvg', 'marketCap']
    for ticker in tickers:
        tick = []
        for point in points:
            tick.append(info[ticker]['fundamental'][point])
        data.append(tick)
    # removes the pkl file
    os.remove(file)

df = pd.DataFrame(data, columns=points)
for n in points:
    mask = df[n] != 0
    df = df[mask]
