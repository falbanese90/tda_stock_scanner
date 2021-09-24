from chart import chart, plot
from models import Equity
import json

with open('tickers.json', 'r') as file:
    tickers = json.load(file)

positive_momentum = []
    
for n in tickers['tickers']:
    try:
        stock = chart(n)
    except IndexError:
        pass
    
    e = Equity(stock)
    if e.ma10 >= e.ma20:
        positive_momentum.append(n)
    

positive_momentum = {'positive_momentum': positive_momentum}
with open('positive_momentum.json', 'w') as file:
    json.dump(positive_momentum, file)




