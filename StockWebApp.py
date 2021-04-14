import streamlit as st
import pandas as pd
from PIL import Image
from DEMA import plot_DEMA
from OBV import plot_OBV
from SMA import plot_SMA
import streamlit.components.v1 as components

# ADD title and image
st.write("""
# Stock Market Web Application 
**Stock price data** , date range from Jan 22,2020 to Jan 22, 2021
""")


image = Image.open(
    "logodesign1.png")

st.image(image, use_column_width=True)


# ADD side bar header
st.sidebar.header('User Input')

# Create a function to get user imput


def get_input():
    start_date = st.sidebar.text_input("Start date", "2020-01-22")
    end_date = st.sidebar.text_input("End date", "2021-01-22")
    stock_symbol = st.sidebar.text_input("Stock Symbol", "AMZN")
    strategy_choices = ('DEMA', 'OBV', 'SMA')
    selected_strategy = st.sidebar.selectbox('Chosen strategy', strategy_choices)
    return start_date, end_date, stock_symbol, selected_strategy

# Create a function to get the comapny name


def get_company_name(symbol):
    if symbol == 'AMZN':
        return 'AMZN'
    elif symbol == 'TSLA':
        return 'Tesla'
    elif symbol == 'GOOG':
        return 'AlpMZNhabat'
    elif symbol == 'AAPL':
        return 'Apple'
    else:
        'Not Avaliable'

# Create a function to get the comapny price data and selected timeframe


def get_data(symbol, start, end):

    # Load the data
    if symbol.upper() == 'AMZN':
        df = pd.read_csv('data/AMZN.csv')
    elif symbol.upper() == 'TSLA':
        df = pd.read_csv("data/TSLA.csv")
    elif symbol.upper() == 'GOOG':
        df = pd.read_csv("data/GOOG.csv")
    elif symbol.upper() == 'AAPL':
        df = pd.read_csv("data/AAPL.csv")
    else:
        "Not Found"

    # Get the data range
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

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
company_name = get_company_name(symbol.upper())


# Display the close prices
st.header(company_name+" Close Price\n")
st.line_chart(df['Close'])

# Display the volume
st.header(company_name+" Volume\n")
st.line_chart(df['Volume'])

if chosen_strategy == 'DEMA':
    DEMA_plot_obj = plot_DEMA(df,symbol)
    st.write(DEMA_plot_obj)
    with open("broker_fig.html", "r", encoding='utf-8') as f:
        components.html(f.read(),height=275)
elif chosen_strategy == 'OBV':
    OBV_plot_obj = plot_OBV(df,symbol)
    st.write(OBV_plot_obj)
    with open("broker_fig.html", "r", encoding='utf-8') as f:
        components.html(f.read(),height=275)
else:
    SMA_plot_obj = plot_SMA(df,symbol)
    st.write(SMA_plot_obj)
    with open("broker_fig.html", "r", encoding='utf-8') as f:
        components.html(f.read(),height=275)

# Get statistica on the data
st.header('Data Statistics')
st.write(df.describe())
