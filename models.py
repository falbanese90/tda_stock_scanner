from retrieve_input import fetch_cleaned_tickers

tickers = fetch_cleaned_tickers()

class Equity:
    def __init__(self, info):
        for key, value in info.items():
            if key == 'Symbol':
                self.symbol = value
            elif key == 'Name':
                self.fullname = value
            else:
                pass

    def __repr__(self):
        return f"{self.symbol}"

equities = []
for ticker in tickers:
    t = Equity(ticker)
    equities.append(t)