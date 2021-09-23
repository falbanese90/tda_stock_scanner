import re
import os
import time
import pandas as pd


def time_as_name(filetype=None):
    if filetype:
        f_name = time.asctime() + filetype
    else:
        f_name = time.asctime()
    f_name = re.sub(":", "_", f_name)
    f_name = re.sub(' ', '_', f_name)
    return f_name

def cleanTickers(tickers):
    for n in tickers:
        if len(n) <= 4:
            tickers.append(n)
    return tickers

def retrieve_tickers(file):
    bucket = pd.read_csv(file)
    bucket = bucket['Symbol']
    tickers = []
    for n in bucket:
        tickers.append(n)
    tickers = cleanTickers(tickers)
    return tickers

