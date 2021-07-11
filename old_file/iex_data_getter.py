#import pandas as pd
import requests
#import json
#from config import IEX_TOKEN

class IEXStock:

    def __init__(self, token, symbol):
        self.BASE_URL = 'https://cloud.iexapis.com/v1'
        self.token = token
        self.symbol = symbol

    def get_symbols(self):
        url = f"{self.BASE_URL}/ref-data/symbols?token={self.token}"
        r = requests.get(url)

        return r.json()

    ## getting the historical data from now
    def getOHLC(self,start = None ,end = None,range = False):
        if range:
            url = f"{self.BASE_URL}/time-series/HISTORICAL_PRICES/{self.symbol}?range=3y&sort=ASC&token={self.token}"
            r = requests.get(url)
        else:
            url = f"{self.BASE_URL}/time-series/HISTORICAL_PRICES/{self.symbol}?from={start}&to={end}&sort=ASC&token={self.token}"
            r = requests.get(url)

        return r.json()

"""
stock = IEXStock(IEX_TOKEN,"AAPL")
dict1 = stock.getOHLC('2021-06-01','2021-06-03')
df = pd.DataFrame(dict1)
df = df[['date','uclose','uhigh','ulow','uopen','fclose','uvolume','symbol']]
def datetime2str(time):
    return time.strftime('%d-%m-%Y')
df['date'] = pd.to_datetime(df['date'], unit='ms').apply(datetime2str)
df.set_axis(['Date','Open','High','Low','Close','Adj Close','Volume','symbol'], axis='columns',inplace= True)
df.set_index(pd.DatetimeIndex(df['Date'].values),inplace= True)
print(df)
"""


'''

## getting the stock name 
stock = IEXStock(IEX_TOKEN,"AAPL")
print(stock.get_symbols())

stock_dict = dict()
for company in stock.get_symbols():
    symbol = company['symbol']
    company_name = company['name']
    stock_dict[symbol] = company_name

with open('stock_names.json','w') as f :
    json.dump(stock_dict,f)

with open('stock_names.json','r') as f :
    stock_dict1 = json.load(f)
    print(stock_dict1)
    
'''
