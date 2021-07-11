import streamlit as st
import pymongo
import os
import json
import logging
from src.iex import IEXstock
from datetime import datetime, timedelta, timezone

## helper function
def format_number(num):
    return f"{num:,}"

# Create a function to get the company name
def get_company_name(symbol):
    if symbol in stock_dict.keys():
        return stock_dict[symbol]

def create_cache(data,key):
    cached_obj = dict()
    cached_obj['data'] = data
    cached_obj['cache_key'] = key
    cached_obj['expireAt'] = datetime.now(timezone.utc) + timedelta(hours=24)
    return cached_obj

def connectDB():
    dbName = 'projectValHubDB'
    colName = 'stockFundaData'
    dbConn = pymongo.MongoClient(os.environ["MONGO_URL"])
    db = dbConn[dbName]
    collection = db[colName]
    # create index for query and auto expire
    collection.create_index([('cache_key', 1)])
    collection.create_index([('expireAt', 1)], expireAfterSeconds=0)
    return collection


## client = redis.Redis(host="localhost", port=6379)

screen = st.sidebar.selectbox(
    "View", ('Overview', 'Fundamentals', 'News', 'Ownership','Strategy'), index=1)
st.title(screen)

#logging.info(os.getcwd())
## get this file location
dir = os.path.dirname(__file__)
filename = os.path.join(dir,'src','stock_names.json')
with open(filename) as f :
    stock_dict = json.load(f)
symbol = st.sidebar.selectbox("Stock Symbol",list(stock_dict.keys()))

failure = 1
while(failure):
    try:
        stock = IEXstock(os.environ["IEX_TOKEN"], symbol)
        failure = 0
    except Exception as e:
        logging.info(e)

if screen == 'Overview':
    collection = connectDB()
    logo_cache_key = f"{symbol}_logo"
    cached_logo = collection.find_one({'cache_key':logo_cache_key},{ "_id": 0,'cache_key':0,'expireAt':0})

    if cached_logo is not None:
        logging.info("found logo in cache")
    else:
        logging.info("getting logo from api, and then storing it in cache")
        cached_logo = create_cache(stock.get_logo(),logo_cache_key)
        collection.insert_one(cached_logo)
    logo = cached_logo['data']

    company_cache_key = f"{symbol}_company"
    cached_company_info = collection.find_one({'cache_key':company_cache_key},{ "_id": 0,'cache_key':0,'expireAt':0})

    if cached_company_info is not None:
        logging.info("found company news in cache")
    else:
        logging.info("getting company from api, and then storing it in cache")
        cached_company_info = create_cache(stock.get_company_info(),company_cache_key)
        collection.insert_one(cached_company_info)

    company = cached_company_info['data']
    col1, col2 = st.beta_columns([1, 4])

    with col1:
        st.image(logo['url'])

    with col2:
        st.subheader(company['companyName'])
        st.write(company['industry'])
        st.subheader('Description')
        st.write(company['description'])
        st.subheader('CEO')
        st.write(company['CEO'])


if screen == 'News':
    collection = connectDB()
    news_cache_key = f"{symbol}_news"
    cached_news = collection.find_one({'cache_key': news_cache_key}, {"_id": 0,'cache_key':0,'expireAt':0})

    if cached_news is not None:
        logging.info("found news in cache")
    else:
        cached_news = create_cache(stock.get_company_news(),news_cache_key)
        collection.insert_one(cached_news)

    news = cached_news['data']

    for article in news:
        st.subheader(article['headline'])
        dt = datetime.utcfromtimestamp(article['datetime']/1000).isoformat()
        st.write(f"Posted by {article['source']} at {dt}")
        st.write(article['url'])
        st.write(article['summary'])
        st.image(article['image'])


if screen == 'Fundamentals':
    collection = connectDB()
    stats_cache_key = f"{symbol}_stats"
    cached_stats = collection.find_one({'cache_key': stats_cache_key}, {"_id": 0,'cache_key':0,'expireAt':0})
    if cached_stats is None:
        cached_stats = create_cache(stock.get_stats(),stats_cache_key)
        collection.insert_one(cached_stats)
    else:
        logging.info("found stats in cache")

    stats = cached_stats['data']

    st.header('Ratios')

    col1, col2 = st.beta_columns(2)

    with col1:
        st.subheader('P/E')
        st.write(stats['peRatio'])
        st.subheader('Forward P/E')
        st.write(stats['forwardPERatio'])
        st.subheader('PEG Ratio')
        st.write(stats['pegRatio'])
        st.subheader('Price to Sales')
        st.write(stats['priceToSales'])
        st.subheader('Price to Book')
        st.write(stats['priceToBook'])
    with col2:
        st.subheader('Revenue')
        st.write(format_number(stats['revenue']))
        st.subheader('Cash')
        st.write(format_number(stats['totalCash']))
        st.subheader('Debt')
        st.write(format_number(stats['currentDebt']))
        st.subheader('200 Day Moving Average')
        st.write(stats['day200MovingAvg'])
        st.subheader('50 Day Moving Average')
        st.write(stats['day50MovingAvg'])

    fundamentals_cache_key = f"{symbol}_fundamentals"
    cached_fundamentals = collection.find_one({'cache_key': fundamentals_cache_key}, {"_id": 0,'cache_key':0,'expireAt':0})

    if cached_fundamentals is None:
        cached_fundamentals = create_cache(stock.get_fundamentals('quarterly'),fundamentals_cache_key)
        collection.insert_one(cached_fundamentals)
    else:
        logging.info("found fundamentals in cache")

    fundamentals = cached_fundamentals['data']


    for quarter in fundamentals:
        st.header(f"Q{quarter['fiscalQuarter']} {quarter['fiscalYear']}")
        st.subheader('Filing Date')
        st.write(quarter['filingDate'])
        st.subheader('Revenue')
        st.write(format_number(quarter['revenue']))
        st.subheader('Net Income')
        st.write(format_number(quarter['incomeNet']))

    st.header("Dividends")

    dividends_cache_key = f"{symbol}_dividends"
    cached_dividends = collection.find_one({'cache_key': dividends_cache_key}, {"_id": 0,'cache_key':0,'expireAt':0})

    if cached_dividends is None:
        cached_dividends = create_cache(stock.get_dividends(),dividends_cache_key)
        collection.insert_one(cached_dividends)
    else:
        logging.info("found dividends in cache")

    dividends = cached_dividends['data']

    for dividend in dividends:
        st.write(dividend['paymentDate'])
        st.write(dividend['amount'])

if screen == 'Ownership':
    collection = connectDB()
    st.subheader("Institutional Ownership")

    institutional_ownership_cache_key = f"{symbol}_institutional"
    cached_institutional_ownership = collection.find_one({'cache_key': institutional_ownership_cache_key}, {"_id": 0,'cache_key':0,'expireAt':0})

    if cached_institutional_ownership is None:
        cached_institutional_ownership = create_cache(stock.get_institutional_ownership(),institutional_ownership_cache_key)
        collection.insert_one(cached_institutional_ownership)

    else:
        logging.info("getting inst ownership from cache")

    institutional_ownership = cached_institutional_ownership['data']
    for institution in institutional_ownership:
        st.write(institution['date'])
        st.write(institution['entityProperName'])
        st.write(institution['reportedHolding'])

    st.subheader("Insider Transactions")

    insider_transactions_cache_key = f"{symbol}_insider_transactions"
    cached_insider_transactions = collection.find_one({'cache_key': insider_transactions_cache_key}, {"_id": 0,'cache_key':0,'expireAt':0})

    if cached_insider_transactions is None:
        cached_insider_transactions = create_cache(stock.get_insider_transactions(),insider_transactions_cache_key)
        collection.insert_one(cached_insider_transactions)

    else:
        logging.info("getting insider transactions from cache")

    insider_transactions = cached_insider_transactions['data']

    for transaction in insider_transactions:
        st.write(transaction['filingDate'])
        st.write(transaction['fullName'])
        st.write(transaction['transactionShares'])
        st.write(transaction['transactionPrice'])

if screen == 'Strategy':
    from src.StreamStrat import run
    run(symbol,get_company_name(symbol))

