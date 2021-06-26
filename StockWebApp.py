import streamlit as st
import os
import pandas as pd
import json
import pymongo
from PIL import Image
from DEMA import plot_DEMA
from OBV import plot_OBV
from SMA import plot_SMA
from iex_data_getter import IEXStock
from datetime import timedelta,date
# from config import mongo_connect_str,IEX_TOKEN


##helper function
def datetime2str(time):
    return time.strftime('%Y-%m-%d')

#stock_dict = {'AAPL': 'Apple Inc.', 'MSFT': 'Microsoft Corporation', 'AMZN': 'Amazon.com, Inc.',
#              'GOOG': 'Alphabet Inc.', 'FB': 'Facebook, Inc.', 'TSLA': 'Tesla, Inc.',
#              'BABA': 'Alibaba Group Holding Limited', 'TSM': 'Taiwan Semiconductor Manufacturing Company Limited',
#              'JPM': 'JPMorgan Chase & Co.', 'NVDA': 'NVIDIA Corporation', 'DIS': 'The Walt Disney Company',
#              'KO': 'The Coca-Cola Company', 'VZ': 'Verizon Communications Inc.', 'INTC': 'Intel Corporation',
#              'NFLX': 'Netflix, Inc.', 'PFE': 'Pfizer Inc.', 'BA': 'The Boeing Company', 'SE': 'Sea Limited',
#              'SQ': 'Square, Inc.', 'AMD': 'Advanced Micro Devices, Inc.', 'ZM': 'Zoom Video Communications, Inc.',
#              'ABNB': 'Airbnb, Inc.', 'GM': 'General Motors Company', 'NIO': 'NIO Inc.', 'F': 'Ford Motor Company',
#              'PLTR': 'Palantir Technologies Inc.', 'GME': 'GameStop Corp.', 'AMC': 'AMC Entertainment Holdings, Inc.',
#              'BYND': 'Beyond Meat, Inc.', 'BB': 'BlackBerry Limited'}



with open('stock_names.json','r') as f :
    stock_dict = json.load(f)


# ADD title and image
today = date.today()
threeYrsAgo = today - timedelta(days = 3*365)
st.write(f"""
# Stock Market Web Application 
**Stock price data** , date range from {threeYrsAgo.strftime('%b %d, %Y')} to {today.strftime('%b %d, %Y')}
""")


image = Image.open(
    "logodesign1.png")

st.image(image, use_column_width=True)


# ADD side bar header
st.sidebar.header('User Input')

# Create a function to get user input


def get_input():
    start_date = st.sidebar.date_input("Start date", threeYrsAgo)
    end_date = st.sidebar.date_input("End date", today)
    stock_symbol = st.sidebar.selectbox("Stock Symbol",list(stock_dict.keys()))
    strategy_choices = ('DEMA', 'OBV', 'SMA')
    selected_strategy = st.sidebar.selectbox('Chosen strategy', strategy_choices)

    stake = st.sidebar.slider('Stake', 100, 1000, 1000, 100)
    cash = st.sidebar.slider('Cash', 100000, 1000000, 100000 , 100000)

    return start_date, end_date, stock_symbol, selected_strategy,stake ,cash

# Create a function to get the company name


def get_company_name(symbol):
    if symbol in stock_dict.keys():
        return stock_dict[symbol]
    else:
        'Not Available'

# Create a function to get the company price data and selected timeframe

#def get_data(symbol, start, end):
#
    # Load the data
#    if symbol in stock_dict.keys():
#        df = pd.read_csv(f"data/{symbol}.csv")
#    else:
#        "Not Found"

    # Get the data range
#    #start = pd.to_datetime(start)
#    #end = pd.to_datetime(end)

#    # Set the start and end index row to 0
#    start_row = 0
#    end_row = 0

    # Match the user selection (date) to the date in dataset (search start date)
#    for i in range(0, len(df)):
#        if start <= pd.to_datetime(df['Date'][i]):
#            start_row = i
#            break
    # Match the user selection (date) to the date in dataset (search end date)
#    for j in range(0, len(df)):
#        if end >= pd.to_datetime(df['Date'][len(df)-1-j]):
#            end_row = len(df)-1-j
#            break
    # Set the index to be the date
#    df.set_index(pd.DatetimeIndex(df['Date'].values),inplace= True)

#    return df.iloc[start_row:end_row + 1, :]

def get_data(symbol, start, end):
    dbName = 'projectValHub'
    colName = 'stockPriceData'
    dbConn = pymongo.MongoClient(os.environ["MONGO_URL"])
    db = dbConn[dbName]
    collection = db[colName]
    ## index for sorting
    collection.create_index(([("date_obj", 1)]))

    if collection.count_documents({'symbol':symbol}) >0:
        last = collection.find({'symbol':symbol},{ "_id": 0}).sort("date_obj", -1).limit(1)
        startNew = list(last)[0]['Date']
        delta1 = timedelta(days=3)
        if (pd.to_datetime(end)-pd.to_datetime(startNew)) > delta1:
            stock = IEXStock(os.environ["IEX_TOKEN"], symbol)
            dict1 = stock.getOHLC(startNew, str(end))
            df = pd.DataFrame(dict1)
            df = df[['date', 'uclose', 'uhigh', 'ulow', 'uopen', 'fclose', 'uvolume','symbol']]
            df['date'] = pd.to_datetime(df['date'], unit='ms').apply(datetime2str)
            df.set_axis(['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume','symbol'], axis='columns', inplace=True)
            df['date_obj'] = pd.to_datetime(df['Date'])
            collection.insert_many(df.to_dict('records'))
    else:
        stock = IEXStock(os.environ["IEX_TOKEN"], symbol)
        ## get recent 2yrs data
        dict1 = stock.getOHLC(range = True)
        df = pd.DataFrame(dict1)
        df = df[['date', 'uclose', 'uhigh', 'ulow', 'uopen', 'fclose', 'uvolume','symbol']]
        df['date'] = pd.to_datetime(df['date'], unit='ms').apply(datetime2str)
        df.set_axis(['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume','symbol'], axis='columns', inplace=True)
        df['date_obj'] = pd.to_datetime(df['Date'])
        collection.insert_many(df.to_dict('records'))


def load_data(symbol, start, end):
    dbName = 'projectValHub'
    colName = 'stockPriceData'
    dbConn = pymongo.MongoClient(os.environ["MONGO_URL"])
    db = dbConn[dbName]
    collection = db[colName]
    ## testing sorting
    table = collection.find({'symbol':symbol,"date_obj": {"$gte": pd.to_datetime(start), "$lt": pd.to_datetime(end)}
                     },{ "_id": 0,'symbol':0})
    df = pd.DataFrame(list(table))
    df.set_index("date_obj",drop = True,inplace= True)
    df.index.name = 'index'
    return df


# Set the index to be the date
start, end, symbol , chosen_strategy, stake ,cash = get_input()
# download the data
get_data(symbol, start, end)
## get data from db
df = load_data(symbol, start, end)
# Get the company name
company_name = get_company_name(symbol)


# Display the close prices
st.header(company_name+" Close Price\n")
st.line_chart(df['Close'])

# Display the volume
st.header(company_name+" Volume\n")
st.line_chart(df['Volume'])

if chosen_strategy == 'DEMA':
    plot_obj,model,trade_stats = plot_DEMA(df,symbol, stake ,cash)
elif chosen_strategy == 'OBV':
    plot_obj,model,trade_stats = plot_OBV(df,symbol, stake ,cash)
else:
    plot_obj,model,trade_stats = plot_SMA(df,symbol, stake ,cash)
## handling case of no trade happened
if trade_stats:
    st.bokeh_chart(plot_obj,use_container_width=True)

    #broker_fig = Image.open("broker_fig.png")
    #st.image(broker_fig, use_column_width=True)
    st.bokeh_chart(model,use_container_width=True)

    ## create trade stats table
    st.header('Trades Statistics')
    df_stats1 = pd.DataFrame(trade_stats['result1'])
    df_stats2 = pd.DataFrame(trade_stats['result2'])

    table1 = df_stats1.pivot(index=['id1', 'id2'], columns='col', values='val')
    table2 = df_stats2.pivot(index=['id1', 'id2'], columns='col', values='val')
    table1.sort_values(by='id1', ascending=False, kind='heapsort', inplace=True)
    table2.sort_values(by='id1', ascending=False, kind='heapsort', inplace=True)
    col1, col2 = st.beta_columns(2)
    with col1:
        st.table(table1)
    with col2:
        st.table(table2)
else:
    st.bokeh_chart(plot_obj,use_container_width=True)
    st.markdown("<h3 style='text-align: center;'><strong>No Trade Happened.</strong></h3>", unsafe_allow_html=True)

# Get statistics on the data
#st.header('Data Statistics')
#st.write(df.describe())



