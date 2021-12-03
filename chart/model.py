from .chart import price, plot
from .vol_premium import iv_prem as vol
from .toolbox import timer
import pandas as pd

class Equity():
    @timer
    def __init__(self, ticker):
        self.name = price(ticker.upper())['fundamental']['symbol']
        self.fundamental = price(ticker.upper())['fundamental']
        self.price = price(ticker.upper())['chart']['close'].iloc[-1]
        self.chart = price(ticker.upper())['chart']
        self.hist_vol = vol(ticker.upper())['historical_vol']

    def _plot(self, save_png=False):
        plot(self.chart, self.name, save_png)

    def _export(self):
            self.chart.to_csv(f'{self.name}.csv')

    @property
    def vol_prem(self):
        if vol(self.name.upper())['premium'] == None:
            return str(None)
        else:
            return vol(self.name.upper())['premium']
    
    @property
    def iv(self):
        if vol(self.name.upper())['implied_vol'] == None:
            return str(None)
        else:
            return vol(self.name.upper())['implied_vol']

    def __str__(self):
        return (f'{self.name}: {self.price}\n'
               f'Historical Vol: {self.hist_vol}\n'
               f'Implied Vol: {self.iv}\n'
               f'Vol Premium: {self.vol_prem}\n')
    


