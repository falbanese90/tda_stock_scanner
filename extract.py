import re
import pickle as pkl
from config import ameritrade
import os
import requests
import time
from retrieve_input import fetch_cleaned_tickers

with open('instrument_list.pkl', 'rb') as f:
    columns = pkl.load(f)

tickers = fetch_cleaned_tickers()
url = 'https://api.tdameritrade.com/v1/instruments'
payload = {'apikey': ameritrade,
           'symbol': tickers,
           'projection': 'fundamental'}
tickers = fetch_cleaned_tickers()

info = {'tickers': tickers,
        'payload': payload,
        'columns': columns,
        'url': url}

def store_data(info):
    start = 0
    end = 50
    files = list()
    while start < len(tickers):
        result= requests.get(url, params=payload)
        data = result.json()
        f_name = time.asctime() + '.pkl'
        f_name = re.sub(':', '_', f_name)
        f_name = re.sub(' ', '_', f_name)
        files.append(f_name)
        with open(f_name, 'wb') as file:
            pkl.dump(file)
        start = end
        end += 50
        time.sleep(1)
        os.remove(file)
    
    
    
    
