import pandas as pd

## display the CSV file content.
def display_csv_file(csv_file_path):
    # dump the csf file content for debugging purpose
    csv_file_df = pd.read_csv(csv_file_path, delimiter='|')
    cur_option = pd.get_option('display.max_rows')
    pd.set_option('display.max_rows', None)
    print(csv_file_df)
    pd.set_option('display.max_rows', cur_option)