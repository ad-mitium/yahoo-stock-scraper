import os
import platform
from time import localtime, strftime
from datetime import date

##### Outputting data to file #####
def write_data(url, merge_file_test, data_output_path, is_unit_test=False):

    # Get time in HH-MM-SS format
    time_data = strftime('%H:%M:%S',localtime()) 

    # Get date in YYYY-MM-DD format
    date_data = date.today()
    current_date = str(date_data)

    # Open output file for writing
    data_outfile = open( data_output_path , 'a')

    ##### Get data from web #####
    if (not is_unit_test):    # Actual attempt to scrape
        content = scraper(url)     

        # Check if merge_file is true, then don't add current date to data in output
        if merge_file_test: 
            data_outfile.write(f'{current_date} {time_data}:  {content}') # All output taken daily, with date/time noted
        else:
            data_outfile.write(f'{time_data}:  {content}') # All output recorded on same date and only time noted
    else:
        data_outfile.write(f'Unit test at {time_data} on {current_date}')
    data_outfile.write('\n')
    data_outfile.close()

    return (data_output_path)

##### Create the output file path and filename depending on merge_file flag #####
def create_output_filepath(alt_stock_id,merge_file_test,data_subfolder_path,data_folder_base_path):
    ##### Formatting data file path and filename #####
    # Get date in YYYY-MM-DD format
    date_data = date.today()
    current_date = str(date_data)

    # Craft base folder path, data path, data subfolder and filename
    os_check = platform.system()
#    print(os_check)  # Diagnostic check
    user = os.getlogin()
    if os_check == "Linux":
        base_folder_path = '/home/'+user+'/Documents/Code/' # python scraper base path
        
    else: # Windows stub, need to test this
        base_folder_path = 'C:\\Users\\'+user+'\\Documents\\Code'

    # Check if merge_file is true, then add current date to filename
    if merge_file_test: 
        file_name = alt_stock_id+'.csv'
    else:
        file_name = alt_stock_id+'_'+current_date+'.csv'

    # Merge output path together 
    output_path = os.path.join(base_folder_path,data_folder_base_path,data_subfolder_path,file_name)
    return output_path


##### For Unit testing #####
if (__name__ == '__main__'):    # default to gold as url and stock_name
#    from scrape import bs_scraper as scraper

    base_url = 'https://finance.yahoo.com/quote/GC%3DF'
    alt_stock_name = 'Gold'
    merge_file = False     # Expected test case, change to "True" for testing alternative option of one large file
    subfolder_path = 'data/'
    data_folder_output_base_path = 'yahoo-stock-scraper' # folder to put data folder into inside base_folder_path
    unit_test = True     # Disable call to scrape.py

    output_path = create_output_filepath(alt_stock_name,merge_file,subfolder_path,data_folder_output_base_path)
    
    write_data(base_url, merge_file, output_path, unit_test)

    print('Data was written to',output_path)
else:
    from lib.scrape import bs_scraper as scraper # fixes relative path issue when not testing
