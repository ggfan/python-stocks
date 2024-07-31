import os
from datetime import (date, timedelta, datetime)
import pandas as pd
from constants import *
from stock_analysis import(
    StockAnalysis,
)

########################## Application behavior knobs ##########################
STOCK_EXCHANGE_TYPE='nasdaq'  # 'nasdaq' or 'nyse'

# analysis span [ENDING_DAY - DURATION,ENDING_DAY)
ANALYSIS_ENDING_DAY = date.today() + timedelta(1)
ANALYSIS_DURATION = DEFAULT_DAYS_TO_GET_QUOTES

# Should download NADAQ company list (bypassing local caches)
DOWNLOAD_NEW_LIST = False
# should download quotes from yfinance?
DOWNLOAD_NEW_QUOTES = False # False

# final result size and disk writing control
RESULT_LIST_SIZE = DEFAULT_RESULT_PERFORMER_LIST_LEN+10
# write the result lists (top/bottom performers) to file: keep it True
WRITE_RESULT_LIST_TO_DISK = True

################################ Main Routine #################################
def main():
    start_time = datetime.now()    
#    nasdaq = StockAnalysis('nasdaq')
#    performers = nasdaq.anaylze((ANALYSIS_DURATION, ANALYSIS_ENDING_DAY),
#                                result_size = RESULT_LIST_SIZE
#                               )
    
    nyse = StockAnalysis('nyse')
    nyse_performers = nyse.anaylze((ANALYSIS_DURATION, ANALYSIS_ENDING_DAY),
                                result_size = RESULT_LIST_SIZE
                               )
    end_time = datetime.now()
    print(f"App statistics:\n"
          f"  Started @ {start_time},\n"
          f"  Completed @ {end_time},\n"
          f"  Execution time: {end_time - start_time}")

if __name__ == '__main__':
    main()
