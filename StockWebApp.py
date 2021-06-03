import streamlit as st
import pandas as pd
from PIL import Image
from DEMA import plot_DEMA
from OBV import plot_OBV
from SMA import plot_SMA

stock_dict = {'AAPL': 'Apple Inc.', 'MSFT': 'Microsoft Corporation', 'AMZN': 'Amazon.com, Inc.',
              'GOOG': 'Alphabet Inc.', 'FB': 'Facebook, Inc.', 'TSLA': 'Tesla, Inc.',
              'BABA': 'Alibaba Group Holding Limited', 'TSM': 'Taiwan Semiconductor Manufacturing Company Limited',
              'JPM': 'JPMorgan Chase & Co.', 'NVDA': 'NVIDIA Corporation', 'DIS': 'The Walt Disney Company',
              'KO': 'The Coca-Cola Company', 'VZ': 'Verizon Communications Inc.', 'INTC': 'Intel Corporation',
              'NFLX': 'Netflix, Inc.', 'PFE': 'Pfizer Inc.', 'BA': 'The Boeing Company', 'SE': 'Sea Limited',
              'SQ': 'Square, Inc.', 'AMD': 'Advanced Micro Devices, Inc.', 'ZM': 'Zoom Video Communications, Inc.',
              'ABNB': 'Airbnb, Inc.', 'GM': 'General Motors Company', 'NIO': 'NIO Inc.', 'F': 'Ford Motor Company',
              'PLTR': 'Palantir Technologies Inc.', 'GME': 'GameStop Corp.', 'AMC': 'AMC Entertainment Holdings, Inc.',
              'BYND': 'Beyond Meat, Inc.', 'BB': 'BlackBerry Limited'}

# ADD title and image
st.write("""
# Stock Market Web Application 
**Stock price data** , date range from Jun 01,2017 to Jun 01, 2021
""")


image = Image.open(
    "logodesign1.png")

st.image(image, use_column_width=True)


# ADD side bar header
st.sidebar.header('User Input')

# Create a function to get user imput


def get_input():
    start_date = st.sidebar.date_input("Start date", pd.to_datetime("2020-06-01"))
    end_date = st.sidebar.date_input("End date", pd.to_datetime("2021-06-01"))
    stock_symbol = st.sidebar.selectbox("Stock Symbol",list(stock_dict.keys()))
    strategy_choices = ('DEMA', 'OBV', 'SMA')
    selected_strategy = st.sidebar.selectbox('Chosen strategy', strategy_choices)
    return start_date, end_date, stock_symbol, selected_strategy

# Create a function to get the comapny name


def get_company_name(symbol):
    if symbol in stock_dict.keys():
        return stock_dict[symbol]
    else:
        'Not Avaliable'

# Create a function to get the comapny price data and selected timeframe


def get_data(symbol, start, end):

    # Load the data
    if symbol in stock_dict.keys():
        df = pd.read_csv(f"data/{symbol}.csv")
    else:
        "Not Found"

    # Get the data range
    #start = pd.to_datetime(start)
    #end = pd.to_datetime(end)

    # Set the start and end index rown to 0
    start_row = 0
    end_row = 0

    # Match the user selection (date) to the date in dataset (search start date)
    for i in range(0, len(df)):
        if start <= pd.to_datetime(df['Date'][i]):
            start_row = i
            break
    # Match the user selection (date) to the date in dataset (search end date)
    for j in range(0, len(df)):
        if end >= pd.to_datetime(df['Date'][len(df)-1-j]):
            end_row = len(df)-1-j
            break
    # Set the index to be the date
    df = df.set_index(pd.DatetimeIndex(df['Date'].values))

    return df.iloc[start_row:end_row + 1, :]


# Set the index to be the date
start, end, symbol , chosen_strategy = get_input()
# Get the data
df = get_data(symbol, start, end)
# Get the company name
company_name = get_company_name(symbol)


# Display the close prices
st.header(company_name+" Close Price\n")
st.line_chart(df['Close'])

# Display the volume
st.header(company_name+" Volume\n")
st.line_chart(df['Volume'])

if chosen_strategy == 'DEMA':
    plot_obj,model = plot_DEMA(df,symbol)
elif chosen_strategy == 'OBV':
    plot_obj,model = plot_OBV(df,symbol)
else:
    plot_obj,model = plot_SMA(df,symbol)

st.bokeh_chart(plot_obj,use_container_width=True)
#broker_fig = Image.open("broker_fig.png")
#st.image(broker_fig, use_column_width=True)
st.bokeh_chart(model,use_container_width=True)


# Get statistica on the data
st.header('Data Statistics')
st.write(df.describe())
