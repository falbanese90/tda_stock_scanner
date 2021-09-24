

class Equity:
    def __init__(self, ticker):
        self.ticker = ticker['fundamental']['symbol']
        self.peRatio = ticker['fundamental']['peRatio']
        self.ma10 = ticker['chart']['MA10'][-1]
        self.ma20 = ticker['chart']['MA20'][-1]