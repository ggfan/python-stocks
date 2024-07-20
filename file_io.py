import os
from constants import *

# Write the final list files into
#   os.getcwd()/outputs/{input_file_name}
def write_list(fn, list_data):
    # write a list of (ticker, date, percent)
    str_to_write = ""
    for item in list_data:
        (ticker, date, val) = item
        if str_to_write:
            str_to_write += "\r\n"
        str_to_write += ticker + " " + date + " " + str(val)

    out_file_name = os.getcwd() + "/" + OUTPUT_FILE_DIR + fn
    f = open(out_file_name, "w+")
    f.write(str_to_write)
    f.close()
