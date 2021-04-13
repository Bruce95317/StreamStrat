#import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from trader import backtrader_runner

plt.style.use('fivethirtyeight')

#df = pd.read_csv('data/AMZN.csv')

#df = df.set_index(pd.DatetimeIndex(df['Date'].values))


# Create a function to calcualte the Double Exponential Moving Average (DEMA)


def DEMA(data, time_period, column):
    # Calcualte DEMA
    EMA = data[column].ewm(span=time_period, adjust=False).mean()
    DEMA = 2*EMA - EMA.ewm(span=time_period, adjust=False).mean()

    return DEMA


# plot the chart
# create a list of columns to keep

#column_list = ['DEMA_short', 'DEMA_long', 'Close']


# Visually show the clsoe price
#df[column_list].plot(figsize=(12.2, 6.4))
#plt.title('Close Price for Amazon')
#plt.ylabel('USD Price ($)')
# plt.xlabel('Date')
# plt.show()

# Create a function to bus and sell the stock (The trading strtegy)


def DEMA_strategy(data):
    buy_list = []
    sell_list = []
    flag = False
    # Loop through the data
    for i in range(0, len(data)):
        if data['DEMA_short'][i] > data['DEMA_long'][i] and flag == False:
            buy_list.append(data['Close'][i])
            sell_list.append(np.nan)
            flag = True
        elif data['DEMA_short'][i] < data['DEMA_long'][i] and flag == True:
            buy_list.append(np.nan)
            sell_list.append(data['Close'][i])
            flag = False
        else:
            buy_list.append(np.nan)
            sell_list.append(np.nan)

    # store buy and sell signal/lists into the data set
    data['Buy'] = buy_list
    data['Sell'] = sell_list

# Store the short term DEMA (20 day period) and the long term DEMA (50 day period) into the data set

def plot_DEMA(data,stock_name):
    df = data.copy(deep=True)

    df['DEMA_short'] = DEMA(df, 20, 'Close')

    df['DEMA_long'] = DEMA(df, 50, 'Close')

    # Run the stretegy to get the buy and sell signals
    DEMA_strategy(df)

    # put into backtrader
    backtrader_runner(df,'DEMA')

    # Visually show the stocks buy and sell signals

    plot_obj = plt.figure(figsize=(12.2, 4.5))
    ax = plot_obj.gca()
    ax.scatter(df['Buy'].dropna().index, df['Buy'].dropna(), color='green',
                label='Buy Signal', marker='^', alpha=1)
    ax.scatter(df['Sell'].dropna().index, df['Sell'].dropna(), color='red',
                label='sell Signal', marker='v', alpha=1)
    ax.plot(df['Close'], label='Close Price', alpha=0.35)
    ax.plot(df['DEMA_short'], label='DEMA_short', alpha=0.35)
    ax.plot(df['DEMA_long'], label='DEMA_long', alpha=0.35)
    ax.set_title(stock_name + ' Close Price Buy and Sell Signals')
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('Close Price ($)', fontsize=18)
    ax.legend(loc='upper left')
    return plot_obj
