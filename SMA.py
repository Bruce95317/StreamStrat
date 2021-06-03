# Description : use the dual moving average crossover to determin when to buy and sell stock

# import the library
import pandas as pd
import numpy as np
#from datetime import datetime
# import matplotlib.pyplot as plt
from trader import backtrader_runner

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource,HoverTool



#plt.style.use('fivethirtyeight')

# laod the old_data
#AMZN = pd.read_csv('old_data/AMZN.csv')


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
def buy_sell(data):
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

    # Create a new old_data frame ot store all the old_data
    data = df.copy(deep=True)
    data['SMA30'] = SMA30['Adj Close Price']
    data['SMA100'] = SMA100['Adj Close Price']

    # Store the buy and sell old_data into a variable
    buy_sell1 = buy_sell(data)
    data['Buy_Signal_Price'] = buy_sell1[0]
    data['Sell_Signal_Price'] = buy_sell1[1]

    # put into backtrader
    model = backtrader_runner(data,'SMA')
    '''
    plot_obj = plt.figure(figsize=(12.2, 4.5))
    ax = plot_obj.gca()
    ax.plot(old_data['Adj Close'], label='Close Price', alpha=0.35)
    ax.plot(old_data['SMA30'], label='SMA30', alpha=0.35)
    ax.plot(old_data['SMA100'], label='SMA100', alpha=0.35)

    ax.scatter(old_data['Buy_Signal_Price'].dropna().index, old_data['Buy_Signal_Price'].dropna(), color='green',
                label='Buy Signal', marker='^', alpha=1)
    ax.scatter(old_data['Sell_Signal_Price'].dropna().index, old_data['Sell_Signal_Price'].dropna(), color='red',
                label='Sell Signal', marker='v', alpha=1)

    ax.set_title(stock_name + ' Close Price Buy and Sell Signals')
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('Close Price ($)', fontsize=18)
    ax.legend(loc='upper left')
    '''

    source = ColumnDataSource(data=data)

    p = figure(x_axis_type="datetime",plot_height=350)

    p.line(x='index', y = 'Adj Close',line_alpha=0.35, source=source,legend_label="Close Price",line_color = '#1f77b4',line_width = 4 )

    p.line(x='index', y='SMA30', line_alpha=0.35, source=source,legend_label='SMA30',line_color = '#d62728',line_width = 4 )

    p.line(x='index', y='SMA100', line_alpha=0.35, source=source,legend_label='SMA100',line_color = '#ff7f0e',line_width = 4 )

    buy_scatter = p.scatter(x = 'index',y = 'Buy_Signal_Price',marker="triangle",
                            source=source,legend_label='Buy Signal',color='green',size=5)

    sell_scatter = p.scatter(x = 'index' , y = 'Sell_Signal_Price', marker="inverted_triangle",
                             source=source,legend_label='Sell Signal',color='red',size=5)

    p.legend.location = "top_left"
    p.title.text = stock_name + ' Close Price Buy and Sell Signals'
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Close Price USD'

    p.add_tools(
        HoverTool(
            tooltips=[('date','@index{%F}'),('close','$@Close{0.2f}') ],
            formatters = {
                     '@index': 'datetime'
                 },
            mode = "vline",
            renderers = [buy_scatter, sell_scatter])
    )

    return p,model
