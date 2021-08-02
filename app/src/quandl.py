import requests
import pandas as pd
import numpy as np


class QuandlStock:
    def __init__(self, token, symbol):
        self.BASE_URL = "https://www.quandl.com/api/v3/datasets/HKEX"
        self.token = token
        self.symbol = symbol

    def get_stock_price(self,start = None ,end = None):
        url = f"{self.BASE_URL}/{self.symbol}?order=asc&start_date={start}&end_date={end}&api_key={self.token}"
        r = requests.get(url)
        return r.json()["dataset"]["data"]

    def get_symbols(self):
        """
        url = f"https://www.quandl.com/api/v3/databases/HKEX/metadata?api_key={self.token}"
        r = requests.get(url)
        import zipfile, io
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall()
        """
        stock_list = pd.read_csv("HKEX_metadata.csv", usecols=["code","name","description"])
        condit1 = stock_list["description"].str.contains("Stock Prices")
        condit2 = stock_list["description"].str.contains("Currency: HKD")
        stock_list = stock_list[np.logical_and(condit1,condit2)]
        result = dict()
        for code, company_name in zip(stock_list["code"],stock_list["name"]):
            result[code] = company_name

        import json
        with open('hk_stock_name.json', 'w') as fp:
            json.dump(result, fp)
