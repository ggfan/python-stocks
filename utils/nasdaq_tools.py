import pandas_market_calendars as mcal
from datetime import datetime, timedelta

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
