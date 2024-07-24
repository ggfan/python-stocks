import os
from datetime import (date, timedelta, datetime)
import pandas as pd
from constants import *
from utils import (
    get_exchange_tickers,
)
from quotes_calculations import (
    download_stocks,
    convert_quotes_to_percentage_growth,
    filter_quotes,
)

########################## Application behavior knobs ##########################
STOCK_EXCHANGE_TYPE='nasdaq'  # 'nasdaq' or 'nyse'

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
    cwd = os.getcwd()
    tickers = get_exchange_tickers(STOCK_EXCHANGE_TYPE, cwd, DOWNLOAD_NEW_LIST)
    
    stocks = download_stocks(
        STOCK_EXCHANGE_TYPE,
        tickers,
        (ANALYSIS_DURATION, ANALYSIS_ENDING_DAY),
        cwd,
        force_download=DOWNLOAD_NEW_QUOTES
    )

    growths = convert_quotes_to_percentage_growth(
        STOCK_EXCHANGE_TYPE,
        stocks,
        cwd,
        force_recalculating=True
    )

    # Filter the quotes into 4 lists: (ups, steadies, downs, slippers)
    filter_quotes(
        STOCK_EXCHANGE_TYPE,
        growths,
        cwd,
        result_size=RESULT_LIST_SIZE,
        write_file=WRITE_RESULT_LIST_TO_DISK
    )
    
    end_time = datetime.now()
    print(f"App statistics:\n"
          f"  Started @ {start_time},\n"
          f"  Completed @ {end_time},\n"
          f"  Execution time: {end_time - start_time}")

if __name__ == '__main__':
    main()
