"""
import requests
from bs4 import BeautifulSoup as bs
import yfinance as yf

data = yf.download("SPY AAPL", start="2017-01-01", end="2017-04-30")


res = requests.get('https://finance.yahoo.com/u/yahoo-finance/watchlists/most-added')
res.encoding = 'utf-8'
res_html = bs(res.text, "html.parser")

stock_names = [result.text for result in res_html.find_all('td', {'class': "data-col0"})[2:32]]
company_names = [result.text for result in res_html.find_all('td', {'class': "data-col1"})[2:32]]

stock_dict = dict()
for stock_name,company_name in zip(stock_names ,company_names):
    stock_dict[stock_name] = company_name

## getting data from the last 5 years (2017-2021)
for stock_name in stock_names:
    data = yf.download(stock_name, start="2017-06-01", end="2021-06-01")
    data.to_csv(f'data/{stock_name}.csv',float_format='%.5f')
"""


