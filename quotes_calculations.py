from file_io import write_list
from utils import (
    insert_to_ascend_list,
    insert_to_descend_list,
)

# percentage_growths: a dict of percentage growth(ticker, [(date, percent)])
def filter_quotes(percentage_growths, result_size, write_file = False):
    tops = []
    climbers=[]
    bottoms = []
    slippers = []
    count = 0
    for ticker in percentage_growths:
        count += 1
        growths = percentage_growths[ticker]
        average = 0.0
        for growth in growths:
            (date, percent) = growth
            average += percent
        size = len(growths)
        average = round(average/size, 2)
        (date, percent) = growths[size - 1]
        latest_day_change = (ticker, date, percent)
        period_average = (ticker, date, average)
        tops = insert_to_descend_list(tops, latest_day_change, result_size)
        climbers = insert_to_descend_list(climbers, period_average, result_size)
        bottoms = insert_to_ascend_list(bottoms, latest_day_change, result_size)
        slippers = insert_to_ascend_list(slippers, period_average, result_size)

    if write_file == True and len(tops) > 0:
        first_key = next(iter(percentage_growths))
        growths = percentage_growths[first_key]
        tail_idx = len(growths) - 1
        
        name_suffix = growths[0][0] + '-' + growths[tail_idx][0]
        write_list('top-list-' + name_suffix + '.txt', tops)
        write_list('steady-climber-list-' + name_suffix + '.txt', climbers)
        write_list('bottom-list-' + name_suffix + '.txt', bottoms)
        write_list('steady-down-list-'+name_suffix + '.txt', slippers)

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
