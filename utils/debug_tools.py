import pandas as pd
# from nasdaq_tools import load_csv_file

## display the CSV file content.
def display_csv_file(csv_file_path, csv_delimiter='|'):
    # dump the csf file content for debugging purpose
    csv_file_df = pd.read_csv(csv_file_path, delimiter = csv_delimiter)
    csv_file_df.drop(csv_file_df.tail(1).index, inplace=True)
    symbols = csv_file_df.iloc[:, :1]
    cur_option = pd.get_option('display.max_rows')
    pd.set_option('display.max_rows', None)
    print(csv_file_df)
    print(symbols)
    pd.set_option('display.max_rows', cur_option)

    print("===displaying keys=====")
    csv_file_df.keys()
    csv_file_df.info()
    csv_file_df.shape





