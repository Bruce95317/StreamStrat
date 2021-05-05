# Description : use the dual moving average crossover to determin when to buy and sell stock

# import the library
import pandas as pd
import numpy as np
#from datetime import datetime
import matplotlib.pyplot as plt
from trader import backtrader_runner
plt.style.use('fivethirtyeight')

# laod the data
#AMZN = pd.read_csv('data/AMZN.csv')


#plt.figure(figsize=(12.3, 4.5))
#plt.plot(AAPL['Adj Close'], label='AAPL')
#plt.plot(SMA30['Adj Close Price'], label='SMA30')
#plt.plot(SMA100['Adj Close Price'], label='SMA100')
#plt.title('Apple Adj. Close Price History')
# plt.xlabel('Date')
#plt.ylabel('Adj Close Price USD($)')
#plt.legend(loc='upper left')
# plt.show()

# Create a function to signal when to buy and when to sell the asset/stock
def buy_sell(data,stock_name):
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1

    for i in range(len(data)):
        if data['SMA30'][i] > data['SMA100'][i]:
            if flag != 1:
                sigPriceBuy.append(data['Adj Close'][i])
                sigPriceSell.append(np.nan)
                flag = 1
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        elif data['SMA30'][i] < data['SMA100'][i]:
            if flag != 0:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(data['Adj Close'][i])
                flag = 0
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        else:
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(np.nan)

    return(sigPriceBuy, sigPriceSell)


def plot_SMA(df,stock_name):
    # Create the simple moving average with a 30 day window (30 MA)
    SMA30 = pd.DataFrame()
    SMA30['Adj Close Price'] = df['Adj Close'].rolling(window=30).mean()

    # Create the simple moving 100 day average (100 MA)

    SMA100 = pd.DataFrame()
    SMA100['Adj Close Price'] = df['Adj Close'].rolling(window=100).mean()

    # Create a new data frame ot store all the data
    data = df.copy(deep=True)
    data['SMA30'] = SMA30['Adj Close Price']
    data['SMA100'] = SMA100['Adj Close Price']

    # Store the buy and sell data into a variable
    buy_sell1 = buy_sell(data, stock_name)
    data['Buy_Signal_Price'] = buy_sell1[0]
    data['Sell_Signal_Price'] = buy_sell1[1]

    # put into backtrader
    backtrader_runner(data,'SMA')

    plot_obj = plt.figure(figsize=(12.2, 4.5))
    ax = plot_obj.gca()
    ax.plot(data['Adj Close'], label=(stock_name + '_Close'), alpha=0.35)
    ax.plot(data['SMA30'], label='SMA30', alpha=0.35)
    ax.plot(data['SMA100'], label='SMA100', alpha=0.35)
    ax.scatter(data['Buy_Signal_Price'].dropna().index, data['Buy_Signal_Price'].dropna(), color='green',
                label='Buy Signal', marker='^', alpha=1)
    ax.scatter(data['Sell_Signal_Price'].dropna().index, data['Sell_Signal_Price'].dropna(), color='red',
                label='sell Signal', marker='v', alpha=1)

    ax.set_title(stock_name + ' Close Price Buy and Sell Signals')
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('Close Price ($)', fontsize=18)
    ax.legend(loc='upper left')
    return plot_obj