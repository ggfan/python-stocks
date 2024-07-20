from constants import *

# Find the position for the given val in a decending list of tuple
# data:  a list of tuples [(ticker, date, key), (ticker, date, key)].
#        the "key" here is the percentage for quote increse.
# return: the location(idx) the "key" value should be.
#         0: should be the first entry (pre-pend)
#         len(data): key shold be appended
#         other (0, len(data)): location to insert.
def find_loc_decend(data, new_percent):
    loc = len(data)
    for idx in range(len(data)):
        (_, _, percent) = data[idx]
        if (new_percent >= percent):
            # the 1st one smaller than the new val, it is the location(idx).
            loc = idx
            break
    return loc

# Find the location for the val to be inserted to the "data" list;
# the data list is in a ascending order.
# return: [0, len(data)]
def find_loc_ascend(data, val):
    loc = len(data)
    for idx in range(len(data)):
        (_, _, percent) = data[idx]
        if (val <= percent):
            loc = idx
            break
    return loc

# dst: [(ticker, date, quote), ... ]
# item: (ticker, date, quote)
# dst_capacity: maximum size allowded for "dst"
# return:
#   dst: a list of tuples that was passed in.
def insert_to_descend_list(dst, item, dst_capacity=DEFAULT_RESULT_PERFORMER_LIST_LEN):
    (ticker, date, percent) = item
    idx = find_loc_decend(dst, percent)
    cur_len = len(dst)

    if idx == cur_len:
        if cur_len < dst_capacity:
            # list is not full, append it; otherwise ignore it.
            dst.append((ticker, date, percent))
        return dst
    
    if cur_len >= dst_capacity:
        dst.pop()
    
    # insert this one, either in the front, or in the middle.
    dst = [(ticker, date, percent)] + dst if idx == 0 else \
          dst[:idx] + [(ticker, date, percent)] + dst[idx:]
    return dst

def insert_to_ascend_list(dst, item, dst_capacity=DEFAULT_RESULT_PERFORMER_LIST_LEN):
    (ticker, date, percent) = item
    idx = find_loc_ascend(dst, val = percent)
    cur_len = len(dst)
    # if the new item needs to be appended
    if idx == cur_len:
        if idx < dst_capacity:
            dst.append((ticker, date, percent))
        return dst
    # if the new item needs to be prepended
    if cur_len == dst_capacity:
        dst.pop()

    dst = ([(ticker, date, percent)] + dst) if idx == 0 else \
              (dst[:idx] + [(ticker, date, percent)] + dst[idx:])
    return dst
