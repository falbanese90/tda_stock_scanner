from .chart import price, plot
from .vol_premium import iv_prem as vol
from .toolbox import timer

class Equity():
    @timer
    def __init__(self, ticker):
        self.name = price(ticker.upper())['fundamental']['symbol']
        self.fundamental = price(ticker.upper())['fundamental']
        self.price = price(ticker.upper())['chart']['close'].iloc[-1]
        self.chart = price(ticker.upper())['chart']
        self.vol_prem = vol(ticker.upper())['premium']
        self.hist_vol = vol(ticker.upper())['historical_vol']
        self.iv = vol(ticker.upper())['implied_vol']

    def _plot(self):
        plot(self.chart, self.name)

    def __str__(self):
        return (f'{self.name}: {self.price}\n'
               f'Historical Vol: {self.hist_vol}\n'
               f'Implied Vol: {self.iv}\n'
               f'Vol Premium: {self.vol_prem}\n')
    


