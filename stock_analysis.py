# Consolidate analysis to a class
import os
import sys
from ftplib import FTP
import pickle
import pandas as pd
import yfinance
import numpy as np
from datetime import (date, timedelta, datetime)

from constants import *
from utils import (
    insert_to_ascend_list,
    insert_to_descend_list,

    write_list_file
)

class StockAnalysis:
    # global configurations
    __stub_dir__ = os.getcwd() + '/' + STUB_DIR
    __output_dir__ = os.getcwd() + '/' + OUTPUT_FILE_DIR
    __write_file__ = True
    __use_stub__ = True
    def __init__(self, type='nasdaq'):
        self.market_type = type.lower()
        self.listed_companies_csv_stub = self.__assemble_stub_name('_listed.csv')

        self.listed_tickers_stub = self.__assemble_stub_name('_list.pkl')
        self.stock_quotes_stub = self.__assemble_stub_name('_quotes.pkl')

    def __assemble_stub_name(self, suffix):
        p = self.__stub_dir__ + '/' + self.market_type + suffix
        p = os.path.normpath(p)
        return p
    
    def __download_csv(self, force_download=False):
        if force_download or not os.path.exists(self.listed_companies_csv_stub):
            remote_nasdaq_csv_files = {
                            'nasdaq':NASDAQ_LIST_FILE_PATH,
                            'nyse':NYSE_LIST_FILE_PATH
                           }
            remote_path = remote_nasdaq_csv_files[self.market_type]
            ftp = FTP(NASDAQ_FTP_SERVER)
            ftp.login()  # Login as anonymous
            with open(self.listed_companies_csv_stub, 'wb') as f:
                ftp.retrbinary(f'RETR {remote_path}', lambda data: f.write(data))
            ftp.quit()

    # load cvs file, trim its first column which is ticker to a list.
    # return a python array of tickers.
    def __abstract_tickers_list(self, recalculate=False):
        csv_file_df = pd.read_csv(self.listed_companies_csv_stub, delimiter='|')    
        # drop the final row: it is the file generated time, which we do not care.
        csv_file_df.drop(csv_file_df.tail(1).index, inplace=True)
        tickers = csv_file_df.iloc[:, 0].array
        return tickers

    def get_exchange_tickers(self, force_download=False):
        tickers = np.empty((1,1))
        if not force_download and  os.path.exists(self.listed_tickers_stub):
            # retrieve from cache and return.
            with open(self.listed_tickers_stub, 'rb') as f:
                tickers = pickle.load(f)
            
            return tickers
    
        # download and work out the company tickers
        csv_file = self.__download_csv(force_download)
        tickers = self.__abstract_tickers_list()
        tickers = tickers[~pd.isna(tickers)]
        with open(self.listed_tickers_stub, 'wb+') as f:
            pickle.dump(tickers, f)

        return tickers

    def __is_relavent(self, yf_ticker):
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

    # get a requested stock prices for the give stock ticker (company).
    # ticker:  company ticker (for example, aapl)
    # day:  the latest day of the predefined period:
    #       [day - 6, ... day - 1, day)
    # return:
    #   list of tuples (each tuple has 2 items):
    #     [('yyyy-mm-dd', quote), ..., ('yyyy-mm-dd', quote)]
    def __download_quotes_for_one_ticker(self, ticker, period):
        quotes = []
        (duration, end_day) = period
        ticker_data = yfinance.Ticker(ticker)    
        if not self.__is_relavent(yf_ticker=ticker_data):
            return quotes
        start_day = end_day - timedelta(duration)
        history = ticker_data.history(start = start_day, end = end_day)
        if not history.empty:
            dates = [idx.date().strftime("%Y-%m-%d") for idx in history.index]
            this_quotes= history.loc[:, 'Close']
            for idx in range(len(dates)):
                quotes.append((dates[idx], this_quotes.iloc[idx]))
        return quotes

    # download_quotes:
    #   download the stocks for the given stock exchange market tickers
    # exchange_type:
    #   'nasdaq' or 'nyse'
    # tickers: a list/array of stock company tickers
    # period:  a tuple of (duration, end_day) to get stocks. end_day is excluded.
    # work_dir: the working directory, the subdirectory 'file_stubs' is used for cache.
    # force_download:
    #       True: re-download quotes from yahoo-finance and update the cache.
    #       False: simply load from cache (not downloading from yahoo, even the request and
    #              cached duration does not match.)
    # return:
    #    a dictionary of stocks for all valid companies in the given tikers:
    #    {'ticker1': [(date, quote)...(date, quote)], ...
    #     'tickerN': [(date, quote)...(date, quote)], }
    def __get_period_from_quotes(self, stocks):
        idx = 0
        SET_SIZE = 10
        start_delta = timedelta(0)
        end_delta = timedelta(0)
        date_format = "%Y-%m-%d"

        for _, quotes in stocks.items():
            size = len(quotes)
            if size >= 2:
                start_delta += date.today() - datetime.strptime(quotes[0][0], date_format).date()
                end_delta += date.today() - datetime.strptime(quotes[size-1][0], date_format).date()
                idx += 1
            if SET_SIZE >= idx:
                break

        if idx == 0:
            idx += 1    # avoid divid by 0 case.
        end_delta = end_delta / idx
        start_delta = start_delta/idx
        # period is in the format(days(int), end_day(datetime.date type))
        # end_day is not included.
        duration = (start_delta - end_delta).days + 1
        end = date.today() + end_delta + timedelta(1)   # end day is not included
        return (duration, end)

    def download_stocks(self, period, force_download=False):
        stocks = {}
        if not force_download and os.path.exists(self.stock_quotes_stub):
            # use local cache
            with open(self.stock_quotes_stub, 'rb') as f:
                stocks = pickle.load(f)
            stub_period = self.__get_period_from_quotes(stocks)
            duration_diff = abs(stub_period[0] - period[0])
            end_diff = abs((stub_period[1] - period[1]).days)
            if  duration_diff == 0 and end_diff == 0:
                return stocks
            
        tickers = self.get_exchange_tickers()

        for ticker in tickers:
            cur_quotes = self.__download_quotes_for_one_ticker(ticker, period)
            if bool(cur_quotes):
                stocks[ticker] = cur_quotes

        with open(self.stock_quotes_stub, 'wb') as f:
            pickle.dump(stocks, f)

        return stocks
    
    def convert_to_percentage_growth(self, stocks):
        growths_dict = {}
        for ticker, quotes in stocks.items():
            growths = []

            idx = 1
            while  idx < len(quotes):
                # calculate the changes 
                (date, quote) = quotes[idx]
                (_, prev_quote) = quotes[idx-1]

                increment = round((quote - prev_quote) * 100 / prev_quote, 2)
                growths.append((date, increment))
                idx += 1

            growths_dict[ticker] = growths

        return growths_dict
    
    # Retrieve the percentage growth for the given periods
    # period: (duration, end_day)
    def get_percentage_growth(self, period, recalculating=False):
        stocks = self.download_stocks(period)
        return self.convert_to_percentage_growth(stocks)
    
    # percentage_growths: a dict of percentage growth(ticker, [(date, percent)])
    def filter_stocks(self, percentage_growths,
                      result_size=DEFAULT_RESULT_PERFORMER_LIST_LEN,
                      write_file=True):
        tops = []
        climbers=[]
        bottoms = []
        slippers = []
        count = 0
        for ticker in percentage_growths:
            count += 1
            growths = percentage_growths[ticker]
            size = len(growths)
            if size == 0:
                continue
            average = 0.0
            for growth in growths:
                (date, percent) = growth
                average += percent
            average = round(average/size, 2)
            (date, percent) = growths[size - 1]
            latest_day_change = (ticker, date, percent)
            period_average = (ticker, date, average)
            tops = insert_to_descend_list(tops, latest_day_change, result_size)
            climbers = insert_to_descend_list(climbers, period_average, result_size)
            bottoms = insert_to_ascend_list(bottoms, latest_day_change, result_size)
            slippers = insert_to_ascend_list(slippers, period_average, result_size)

        if write_file and len(tops) > 0:
            first_key = next(iter(percentage_growths))
            growths = percentage_growths[first_key]
            tail_idx = len(growths) - 1
            
            name_suffix = growths[0][0] + '-' + growths[tail_idx][0]
            file_dir = self.__output_dir__ + "/" + self.market_type
            files = [
                (file_dir + '-top-list-' + name_suffix + '.txt', tops),
                (file_dir + '-steady-climber-list-' + name_suffix + '.txt', climbers),
                (file_dir + '-bottom-list-' + name_suffix + '.txt', bottoms),
                (file_dir + '-steady-down-list-'+name_suffix + '.txt', slippers),
            ]
            for file in files:
                write_list_file(file[0], file[1])
    
        return (tops, climbers, bottoms, slippers)
    
    # all in one function to get performers.
    def anaylze(self,
                period=(DEFAULT_DAYS_TO_GET_QUOTES, date.today() + timedelta(1)),
                result_size=DEFAULT_RESULT_PERFORMER_LIST_LEN):
        growths = self.get_percentage_growth(period)
        performers = self.filter_stocks(growths, result_size)
        return performers



