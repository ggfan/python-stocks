## NASDAQ
# company list server and directory
NASDAQ_FTP_SERVER = 'ftp.nasdaqtrader.com'
NASDAQ_LIST_FILE_PATH = '/symboldirectory/nasdaqlisted.txt'
NASDAQ_OTHER_LIST_FILE_PATH = '/symboldirectory/otherlisted.txt'
NYSE_LIST_FILE_PATH = NASDAQ_OTHER_LIST_FILE_PATH
# local file for the nasdaw company list.
NASDAQ_LOCAL_LIST_DIR='lists/'
NASDAQ_LOCAL_LIST_FILE ='nasdaq_listed.txt'
NASDAQ_LOCAL_OTHER_LIST_FILE = 'nasdaq_other_listed.txt'
NYSE_LOCAL_LIST_FILE = NASDAQ_LOCAL_OTHER_LIST_FILE

# trading calendar
# https://business.nasdaq.com/trade/US-Options/Holiday-Trading-Hours.html

## NASDAQ company filter: technology sector, and market_value >= $100M
TECH_SECTOR = 'Technology'
MIN_MARKET_CAP = 100000000
DEFAULT_DAYS_TO_GET_QUOTES = 7

# Target list size
DEFAULT_RESULT_PERFORMER_LIST_LEN = 20
OUTPUT_FILE_DIR='outputs/'


# Stubs used as local cache / debugging
STUB_DIR='file_stubs/'
NASDAQ_LIST_STUB_NAME='nasdaq_list.pkl'
NYSE_LIST_STUB_NAME='nyse_list.pkl'

NASDAQ_QUOTES_STUB_NAME='nasdaq_quotes.pkl'
NASDAQ_CHANGES_STUB_NAME='nasdaq_changes_in_percentage.pkl'
NYSE_QUOTES_STUB_NAME='nyse_quotes.pkl'
NYSE_CHANGES_STUB_NAME='nyse_changes_in_percentage.pkl'
