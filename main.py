import os
from datetime import (date, timedelta, datetime)
import pandas as pd
import pickle
from constants import *
from utils import (
    get_nasdaq_tickers,
    download_nasdaq_list_files,
    get_nasdaq_stock,
)
from quotes_calculations import (
    convert_to_percentage_growths,
    filter_quotes,
)

########################## Application behavior knobs ##########################
# analysis span [ENDING_DAY - DURATION,ENDING_DAY)
ANALYSIS_ENDING_DAY = date.today() + timedelta(1)
ANALYSIS_DURATION = DEFAULT_DAYS_TO_GET_QUOTES

# Should download NADAQ company list (bypassing local caches)
DOWNLOAD_NEW_LIST = False
# should download quotes from yfinance?
DOWNLOAD_NEW_QUOTES = True

# final result size and disk writing control
RESULT_LIST_SIZE = DEFAULT_RESULT_PERFORMER_LIST_LEN+10
# write the result lists (top/bottom performers) to file: keep it True
WRITE_RESULT_LIST_TO_DISK = True

################################ Main Routine #################################
def main():
    start_time = datetime.now()

    ## download the nasdaq company list file.
    nasdaq_list_stub_name = os.getcwd() + '/' + STUB_DIR + NASDAQ_LIST_STUB_NAME
    if not DOWNLOAD_NEW_LIST and os.path.exists(nasdaq_list_stub_name):
        # retrieve from cache.
        with open(nasdaq_list_stub_name, 'rb') as f:
            tickers = pickle.load(f)
    else:
        local_list_dir = os.getcwd() + '/' + NASDAW_LOCAL_LIST_DIR
        (nasdaq_list_file, _) = download_nasdaq_list_files(local_list_dir)
        tickers = get_nasdaq_tickers(nasdaq_list_file)
        tickers = tickers[~pd.isna(tickers)]
        with open(nasdaq_list_stub_name, 'wb+') as f:
            pickle.dump(tickers, f)
    stocks = {}
    increases = {}
    nasdaq_quotes_stub_name = os.getcwd() + '/' + STUB_DIR + NASDAQ_QUOTES_STUB_NAME
    nasdaq_changes_stub_name = os.getcwd() + '/' + STUB_DIR + NASDAQ_CHANGES_STUB_NAME
    if  not DOWNLOAD_NEW_QUOTES and \
        os.path.exists(nasdaq_quotes_stub_name) and \
        os.path.exists(nasdaq_changes_stub_name):
        # use local cache
        with open(nasdaq_quotes_stub_name, 'rb') as f:
            stocks = pickle.load(f)
        with open(nasdaq_changes_stub_name, 'rb') as f:
            increases = pickle.load(f)
    else:
        for ticker in tickers:
            quote = get_nasdaq_stock(ticker, ANALYSIS_ENDING_DAY, ANALYSIS_DURATION)
            if bool(quote):
                stocks[ticker] = quote
                increases[ticker] = convert_to_percentage_growths(quote)
        
        with open(nasdaq_quotes_stub_name, 'wb') as f:
            pickle.dump(stocks, f)
        with open(nasdaq_changes_stub_name, 'wb') as f:
            pickle.dump(increases, f)

    # filter the quotes into 4 lists: (ups, steadies, downs, slippers)
    filter_quotes(increases,
                  result_size=RESULT_LIST_SIZE,
                  write_file=WRITE_RESULT_LIST_TO_DISK)
    
    end_time = datetime.now()
    print(f"program started @ {start_time}, \
            completed @ {end_time}, \
            execution time: {end_time - start_time}")

if __name__ == '__main__':
    main()
