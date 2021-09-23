import csv


def fetch_cleaned_tickers(filename='financial_bucket.csv', bucket=None):
    if bucket:
        if bucket.lower() == 'healthcare':
            filename = 'healthcare_bucket.csv'
        elif bucket.lower() == 'energy':
            filename = 'energy_bucket.csv'
        elif bucket.lower() == 'tech':
            filename = 'growth_tech.csv'

    with open(filename) as f:
        reader = csv.DictReader(f)
        tickers = [x for x in reader]
        tickers = list(filter((lambda x: len(x['Symbol']) <=4), tickers))
        return tickers

    

