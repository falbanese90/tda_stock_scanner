from .chart import price, plot
from .vol_premium import iv_prem as vol

class Equity():
    def __init__(self, ticker):
        self.name = price(ticker.upper())['fundamental']['symbol']
        self.fundamental = price(ticker.upper())['fundamental']
        self.price = price(ticker.upper())['chart']
        self.vol_prem = vol(ticker.upper())['premium']
        self.hist_vol = vol(ticker.upper())['historical_vol']
        self.iv = vol(ticker.upper())['implied_vol']

    def _plot(self):
        plot(self.price, self.name)


