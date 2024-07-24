from file_io import write_list
from utils import (
    insert_to_ascend_list,
    insert_to_descend_list,
    get_nasdaq_stock,
)
from constants import *
import os
import pickle

# percentage_growths: a dict of percentage growth(ticker, [(date, percent)])
def filter_quotes(exchg_type, percentage_growths, work_dir,
                  result_size, write_file = False):
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
        file_dir = work_dir + "/" + OUTPUT_FILE_DIR
        write_list(os.path.normpath(file_dir + exchg_type + '-top-list-' + name_suffix + '.txt'), tops)
        write_list(os.path.normpath(file_dir + exchg_type + '-steady-climber-list-' + name_suffix + '.txt'), climbers)
        write_list(os.path.normpath(file_dir + exchg_type + '-bottom-list-' + name_suffix + '.txt'), bottoms)
        write_list(os.path.normpath(file_dir + exchg_type + '-steady-down-list-'+name_suffix + '.txt'), slippers)

    return (tops, climbers, bottoms, slippers)

# Derive the percentage increase from the give list of quotes.
# quotes: [(date, quote), ..., (date,quote)]
# returns: [(date, percentage increase comparing to the previous day),...]
#          Note that the list will be one item shorter than the input list.
def convert_to_percentage_growths(quotes):
    growths = []

    idx = 1
    while  idx < len(quotes):
        # calculate the changes 
        (date, quote) = quotes[idx]
        (_, prev_quote) = quotes[idx-1]

        increment = round((quote - prev_quote) * 100 / prev_quote, 2)
        growths.append((date, increment))
        idx += 1

    return  growths

# download_stocks:
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

def download_stocks(exchg_type, tickers, period,
                    work_dir, force_download=False):
    quotes_stub_files_dict = {'nasdaq': NASDAQ_QUOTES_STUB_NAME,
                             'nyse': NYSE_QUOTES_STUB_NAME }
    stocks = {}
    (duration, end_day) = period
    stub_name = work_dir + '/' + STUB_DIR + \
                quotes_stub_files_dict[exchg_type.lower()]
    stub_name = os.path.normpath(stub_name)
    
    # finer comparison of the period and cache should be checked later.
    if not force_download and os.path.exists(stub_name):
        # use local cache
        with open(stub_name, 'rb') as f:
            stocks = pickle.load(f)
    else:
        for ticker in tickers:
            cur_quotes = get_nasdaq_stock(ticker, duration, end_day)
            if bool(cur_quotes):
                stocks[ticker] = cur_quotes
        
        with open(stub_name, 'wb') as f:
            pickle.dump(stocks, f)
    return stocks


def convert_quotes_to_percentage_growth(exchg_type, stocks,
                                        work_dir, force_recalculating=False):
    changes_stub_files_dict = {'nasdaq': NASDAQ_CHANGES_STUB_NAME,
                               'nyse': NYSE_CHANGES_STUB_NAME }
    growths_dict = {}
    stub_name = work_dir + '/' + STUB_DIR + changes_stub_files_dict[exchg_type.lower()]
    stub_name = os.path.normpath(stub_name)
    if  not force_recalculating and os.path.exists(stub_name):
        # use local cache
        with open(stub_name, 'rb') as f:
            growths_dict = pickle.load(f)
        return growths_dict
    
    # calculate the grows.
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

    with open(stub_name, 'wb') as f:
        pickle.dump(growths_dict, f)

    return growths_dict

