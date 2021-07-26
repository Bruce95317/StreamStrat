#import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
from trader import backtrader_runner

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource,HoverTool

# plt.style.use('fivethirtyeight')

#df = pd.read_csv('old_data/AMZN.csv')

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

def plot_DEMA(data,stock_name,stake,cash):
    df = data.copy(deep=True)

    df['DEMA_short'] = DEMA(df, 20, 'Close')

    df['DEMA_long'] = DEMA(df, 50, 'Close')

    # Run the stretegy to get the buy and sell signals
    DEMA_strategy(df)

    # put into backtrader
    model,trade_stats = backtrader_runner(df,'DEMA',stake,cash)

    # Visually show the stocks buy and sell signals
    '''
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
    '''

    source = ColumnDataSource(data=df)

    p = figure(x_axis_type="datetime",plot_height=350)

    p.line(x='index', y='Close', line_alpha=0.35, source=source, legend_label="Close Price", line_color='#1f77b4',
           line_width=4)

    p.line(x='index', y='DEMA_short', line_alpha=0.35, source=source, legend_label='DEMA_short', line_color='#d62728',
           line_width=4)

    p.line(x='index', y='DEMA_long', line_alpha=0.35, source=source, legend_label='DEMA_long', line_color='#ff7f0e',
           line_width=4)

    buy_scatter = p.scatter(x='index', y='Buy', marker="triangle",
                            source=source, legend_label='Buy Signal', color='green', size=5)

    sell_scatter = p.scatter(x='index', y='Sell', marker="inverted_triangle",
                             source=source, legend_label='Sell Signal', color='red', size=5)

    p.legend.location = "top_left"
    p.title.text = stock_name + ' Close Price Buy and Sell Signals'
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Close Price USD'

    p.add_tools(
        HoverTool(
            tooltips=[('date', '@index{%F}'), ('close', '$@Close{0.2f}')],
            formatters={
                '@index': 'datetime'
            },
            mode="vline",
            renderers=[buy_scatter, sell_scatter])
    )

    return p,model,trade_stats
