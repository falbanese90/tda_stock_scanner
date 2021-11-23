from chart import chart, options

def iv_prem(ticker):
    ticker = ticker.upper()
    stock = {}
    stock_chart = chart(ticker)['chart']
    stock_iv = options(ticker)
    print(f'Implied Vol: {stock_iv["volatility"]}')
    print(f'Historical Vol: {stock_chart.iloc[-1]["HV"]}')
    result = round(100 * ((stock_iv['volatility'] - stock_chart.iloc[-1]
             ['HV']) / stock_chart.iloc[-1]['HV']), 3)
    print(f'Premium/Discount: {result}')