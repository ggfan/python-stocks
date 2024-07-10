from datetime import (date, timedelta, datetime)
import yfinance
import pandas as pd
from ftplib import FTP
from constants import *
from utils import display_csv_file, is_market_open, get_market_open_days

#https://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs

def download_list_file_from_nasdaq():
    # Download the NASDAQ company file to ./lists/nasdaq_listed.txt
    # and the NYSE to ./lists/nasdaq_other_listed.txt
    list_files =[{'remote': NASDAQ_LIST_FILE_PATH, 'local': NASDAQ_LOCAL_LIST_FILE},
                 {'remote':NYSE_LIST_FILE_PATH, 'local': NYSE_LOCAL_LIST_FILE} ]
    ftp = FTP(NASDAQ_FTP_SERVER)
    ftp.login()  # Login as anonymous
    
    for file in list_files:
        with open(file['local'], 'wb') as f:
            ftp.retrbinary(f'RETR {file['remote']}', lambda data: f.write(data))
    ftp.quit()

def get_stock(ticker, day):
    ticker_data = yfinance.Ticker(ticker)
    history = ticker_data.history(start=day, end=day+timedelta(1))
    info = ticker_data.info
    print("======start of info===========")
    # for key, value in info.items():
    #     print(key, value)
    format = '%Y-%m-%d %H:%M:%S'
    print("SharesShort\t sharesShortPriorMonth \tsharesShortPreviousMonthDate\tsharesShortInterest")
    print(str(info['sharesShort']) + "\t" + str(info['sharesShortPriorMonth']) + "\t" +
          date.fromtimestamp(info['sharesShortPreviousMonthDate']).strftime(format) + '\t' +
          date.fromtimestamp(info['dateShortInterest']).strftime(format))

    print("========end of info===========")
    return history

def main():
    # ticker = "alar"
    # quotes = pd.DataFrame([], columns=['Open'])
    # for idx in range (0, 5):
    #     day = date.today() - timedelta(idx)
    #     quote_of_day = get_stock(ticker, day)
    #     if not quote_of_day.empty:
    #         quotes = pd.concat([quotes, quote_of_day], axis=0)
    
    # print(quotes)
    # nasdaq_tickers = get_nasdaq_company_list()
    #download_list_file_from_nasdaq()
    #display_csv_file(NASDAQ_LOCAL_LIST_FILE)
    #display_csv_file(NYSE_LOCAL_LIST_FILE)

    # today = datetime.now().strftime('%Y-%m-%d')
    # open_days = get_market_open_days(today, 30)
    # for day in open_days:
    #     print(day)


    print("completed")

if __name__ == '__main__':
    main()
