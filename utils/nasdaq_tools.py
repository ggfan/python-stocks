import pandas_market_calendars as mcal
import pandas as pd
import os
from datetime import datetime, timedelta
from constants import *
from ftplib import FTP
import yfinance

# Usage: is_open = is_market_open('2024-07-08')
def is_market_open(date):
    result = mcal.get_calendar("NYSE").schedule(start_date=date, end_date=date)
    return result.empty == False

# return date list for count days before today(today is included)
# start_date:  starting day in 'yyyy-mm-dd' format
# day_count:   number of days before today (including today)
# usage:
#     get_market_open_days('07-09-2024', 10)
# TODO: this version is slow, need implement an more efficient one
def get_market_open_days(start_date, day_count=5):
    format = '%Y-%m-%d'
    #start_date='2024-07-09'
    days = []
    day = datetime.strptime(start_date, format)
    count = 0
    while count < day_count:
        if is_market_open(day.date()):
            days.append(day.strftime(format))
            count += 1

        day -= timedelta(1)

    return days

def load_csv_file(csv_file_path, csv_delimiter='|'):
    csv_file_df = pd.read_csv(csv_file_path, delimiter='|')
    return csv_file_df

# load cvs file, trim its first column which is ticker to a list.
# return a python array of tickers.
def get_nasdaq_tickers(nasdaq_csv_file_path):
    csv_file_df = load_csv_file(nasdaq_csv_file_path, csv_delimiter='|')
    
    # drop the final row: it is the file generated time, which we do not care.
    csv_file_df.drop(csv_file_df.tail(1).index, inplace=True)
    tickers = csv_file_df.iloc[:, 0].array
    return tickers

# download listed companies from NASDAQ. 
# src: https://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs
# dst: dst_list_directory
#      NASDAQ_LOCAL_LIST_FILE
#      NYSE_LOCAL_LIST_FILE
# return:
#     full path for the 2 raw list files.
def download_nasdaq_list_files(dst_list_directory, force_download=False):
    # Download the NASDAQ company file to ./lists/nasdaq_listed.txt
    # and the NYSE to ./lists/nasdaq_other_listed.txt
    dst_nasdaq_file = os.path.normpath(dst_list_directory + '/' + NASDAQ_LOCAL_LIST_FILE)
    dst_nyse_file = os.path.normpath(dst_list_directory + '/' + NYSE_LOCAL_LIST_FILE)
    if (not force_download and
        os.path.exists(dst_nasdaq_file) and
        os.path.exists(dst_nyse_file)):
        #no need to download, use the cache.
        return (dst_nasdaq_file, dst_nyse_file)
    
    # download the files
    list_files =[{'remote': NASDAQ_LIST_FILE_PATH, 'local': dst_nasdaq_file},
                 {'remote':NYSE_LIST_FILE_PATH, 'local': dst_nyse_file} ]
    ftp = FTP(NASDAQ_FTP_SERVER)
    ftp.login()  # Login as anonymous
    
    for file in list_files:
        with open(file['local'], 'wb') as f:
            ftp.retrbinary(f'RETR {file['remote']}', lambda data: f.write(data))
    ftp.quit()
    return (dst_nasdaq_file, dst_nyse_file)

def is_company_relavent(yf_ticker):
    info = yf_ticker.info
    # print(f"{type(info['sector'])} {info['sector']}")
    # print(f"{type(info['marketCap'])} {info['marketCap']}")
    if ('sector' in info and
        info['sector'] == 'Technology' and
        'marketCap' in info
        and info['marketCap'] >= MIN_MARKET_CAP):
        # this is the company we care.
        # [note that yahoo finance sometimes does return the data]
        return True
    
    return False

# get 7 day stock prices for the give stock ticker (company).
# ticker:  company tag on nasdaq (for example, aapl)
# day:  the latest day of the predefined (7 day) period:
#       [day - 6, ... day - 1, day)
# return:
#   list of tuples (each tuple has 2 items):
#     [('yyyy-mm-dd', quote), ..., ('yyyy-mm-dd', quote)]
def get_nasdaq_stock(ticker, end_day, duration=DEFAULT_DAYS_TO_GET_QUOTES):
    stock_quotes = []

    ticker_data = yfinance.Ticker(ticker)    
    if not is_company_relavent(yf_ticker=ticker_data):
        return stock_quotes
    start_day = end_day - timedelta(duration)
    history = ticker_data.history(start = start_day, end = end_day)
    if not history.empty:
        dates = [idx.date().strftime("%Y-%m-%d") for idx in history.index]
        quotes = history.loc[:, 'Close']
        for idx in range(len(dates)):
            stock_quotes.append((dates[idx], quotes.iloc[idx]))
    return stock_quotes


#### Under development functions: TODO: debug it
def get_stock_history(tickers, day):
    # history_df = pd.DataFrame
    history = {}

    idx = 0
    while idx  < len(tickers):
        ticker_set = []
        count = 0
        while idx + count < len(tickers) and count < 10:
            ticker = tickers[idx+count]
            if not pd.isna(ticker):
                ticker_set.append(ticker)
            count += 1
        idx += count
        print(ticker_set)    
        history_subset = yfinance.download(ticker_set, start = day - timedelta(5), period='5d')
        back_row = pd.get_option('display.max_rows')
        back_col = pd.get_option('display.max_columns')
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

        #print(history_subset.columns)
        #print(history_subset.index)
        first_column = history_subset.iloc[:, 20]
        print(first_column)
        pd.set_option('display.max_rows', back_row)
        pd.set_option('display.max_columns', back_col)

        break
        # now need to find a way to concat.
        # history = pd.concat([history, history_subset], axis=0)
    
    # do some debugging...
    print(history)

    return history

    for ticker in tickers:
        # print(f"getting stock for {ticker}:")
        price_history = get_stock(ticker, date.today() - timedelta(1))
        # print(price_history)
        if price_history.empty:
            print(f"Not a valid ticker {ticker}")
            continue
        price = price_history['Close'].iloc[0]
        # print(price)
        print(f"{ticker}: {price}")
