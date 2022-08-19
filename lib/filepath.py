import os
from datetime import date

if (__name__ == '__main__'):    # for unit testing, default to gold as alt_stock_name
    alt_stock_id = 'Gold'
    merge_file = False
    subfolder_path = 'data/'
    data_folder_base_path = 'yahoo-stock-scraper'   # folder to put data folder into inside base_folder_path

def outputfilepath(alt_stock_id,merge_file,subfolder_path,data_folder_base_path):
    ##### Formatting data file path and filename #####
    # Get date in YYYY-MM-DD format
    date_data = date.today()
    current_date = str(date_data)

    # Craft base folder path, data path, data subfolder and filename
    user = os.getlogin()
    base_folder_path = '/home/'+user+'/Documents/Code/' # python scraper base path

    # Check if merge_file is true, then don't add current date to filename
    if merge_file: 
        file_name = alt_stock_id+'.csv'
    else:
        file_name = alt_stock_id+'_'+current_date+'.csv'

    # Merge output path together 
    output_path = os.path.join(base_folder_path,data_folder_base_path,subfolder_path,file_name)
    return output_path


if (__name__ == '__main__'):
    print(outputfilepath(alt_stock_id,merge_file,subfolder_path,data_folder_base_path))