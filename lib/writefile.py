import os
from pathlib import Path
from time import localtime, strftime


##### Outputting data to file #####
def write_data(url, data_output_path, merge_file_test, merge_file_monthly_test, is_unit_test=False):

    # Get time in HH-MM-SS format
    time_data = strftime('%H:%M:%S',localtime())

    # Get date in YYYY-MM-DD format
    current_date = strftime('%Y-%m-%d')

    # Test for year turn over
    if strftime('%m-%d') == '01-01':
        # print("Determine if new year folder exists.")
        test_path(os.path.dirname(data_output_path))

    # Open output file for writing
    if os.path.exists(os.path.dirname(data_output_path)):
        #print(os.path.dirname(data_output_path),data_output_path)
        data_outfile = open( data_output_path , 'a')
    else:
        #print('Failed to find path to data '+ os.path.dirname(data_output_path))
        raise SystemExit('Path to '+data_output_path+' not found')

    ##### Get data from web #####
    if (not is_unit_test):    # Actually attempt to scrape
        content = scraper(url)

        # Check if merge_file is true, then don't add current date to data in output
        if merge_file_test or merge_file_monthly_test:
            data_outfile.write(f'{current_date}_{time_data} {content}\n') # All output taken daily, with date/time noted
        else:
            data_outfile.write(f'{time_data} {content}\n') # All output recorded on same date and only time noted
    else:
        data_outfile.write(f'Unit test at {time_data} on {current_date}\n')
    # data_outfile.write('\n')
    data_outfile.close()

    return (data_output_path)

def write_data_commodities(url, comm_type, base_folder_path, subfolder_path, csv_list_folder, is_unit_test=False):

    # Get time in HH-MM-SS format
    time_data = strftime('%H:%M:%S',localtime())

    # Get date in YYYY-MM-DD format
    current_date = strftime('%Y-%m-%d')

    # Read in list of commodities from csv file
    comm_folder_path=str(Path.home() / 'Documents'/ 'Code')+'/'+base_folder_path+'/'+csv_list_folder+'/'  # This might be a problem if not saved in $USER/Documents/Code
    # print(str(comm_folder_path))
    commodities=csv_reader(comm_folder_path,comm_type)
    # print('Commodities to scrape:',commodities)

    for commodity in commodities.values():
        data_folder_output_path,data_file_name = create_stock_output_filepath(commodity, subfolder_path, base_folder_path, False, True) # Merge monthly
        data_output_path = data_folder_output_path+'/'+data_file_name
        if is_unit_test:
            print('write_data_comm:',is_unit_test, commodity)

        # Open output file for writing
        try:
            data_outfile = open( data_output_path , 'a')    
            ##### Get data from web #####
            if (not is_unit_test):    # Actually attempt to scrape
                web_content = scraper_comm (url,commodities)
                if commodity in web_content:
                    data_outfile.write(f'{current_date}_{time_data}: {web_content[commodity]}\n') 
            else:
                data_outfile.write(f'Unit test at {time_data} on {current_date}\n')
            # data_outfile.write('\n')
        except FileNotFoundError as fnf_error:
            print(fnf_error)
        except IOError:
            print("Unable to open "+data_outfile)

        data_outfile.close()

    # return (data_output_path)



##### For Unit testing #####
if (__name__ == '__main__'):    # default to gold as url and stock_name
#    from scrape import bs_scraper as scraper
    # from scrape import bs_scraper_2 as scraper_comm
    # from random_sleep import sleep_time
    from read_csv import csv_reader 
    from common import create_stock_output_filepath, test_path

    base_url = 'https://finance.yahoo.com/quote/GC%3DF'
    commodities_url='https://finance.yahoo.com/commodities'
    alt_stock_name = 'Gold'
    merge_file = False     # Expected test case, change to "True" for testing alternative option of one large file
    merge_file_monthly = False     # Expected test case, change to "True" for testing alternative option of one large file per month
    use_year = True             # Create year directory, allows for checking csv_config folder
    use_file_name = True        # Useful for creating and testing folders, allows for checking csv_config folder
    subfolder_path = 'data'
    csv_list_folder = 'csv_config_files'
    data_folder_output_base_path = 'yahoo-stock-scraper' # folder to put data folder into inside base_folder_path
    unit_test = True     # Disable calls to scrape.py
    csv_base_folder_path=str(Path().absolute())+'/'+csv_list_folder+'/' # This is only used for unit test, so Path.absolute shouldn't be an issue
    stock_type='fuels'      # change as needed
    # stock_list=csv_reader(csv_base_folder_path, stock_type) 

    output_folder_path,file_name = create_stock_output_filepath(alt_stock_name,subfolder_path,data_folder_output_base_path,merge_file,merge_file_monthly,use_year,use_file_name)
    output_path=output_folder_path+'/'+file_name    # Merge returned output path and filename to pass on to other functions

    write_data(base_url, output_path, merge_file, merge_file_monthly, unit_test)
    write_data_commodities(commodities_url, stock_type, data_folder_output_base_path, subfolder_path, csv_list_folder, unit_test)

    print('Data was written to',output_path)
else:
    from lib.scrape import bs_scraper as scraper # fixes relative path issue when not testing
    from lib.scrape import bs_scraper_2 as scraper_comm 
    from lib.read_csv import csv_reader
    from lib.common import create_stock_output_filepath, test_path
