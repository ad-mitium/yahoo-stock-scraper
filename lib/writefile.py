import os
from pathlib import Path
from time import localtime, strftime

def test_path(output_folder_path):
    if os.path.exists(output_folder_path):
        # print(os.path.dirname(output_folder_path))
        pass
    else:
#        print('Failed to find path to data '+ os.path(data_output_path))
        Path(output_folder_path).mkdir( parents=True, exist_ok=True)
        # raise SystemExit('Path to '+output_folder_path+' not found')

def joinpath(rootdir, targetdir):
    return os.path.join(os.sep, rootdir + os.sep, targetdir)


##### Outputting data to file #####
def write_data(url, data_output_path, merge_file_test, merge_file_monthly_test, is_unit_test=False):

    # Get time in HH-MM-SS format
    time_data = strftime('%H:%M:%S',localtime())

    # Get date in YYYY-MM-DD format
    current_date = strftime('%Y-%m-%d')

    # Open output file for writing
    if os.path.exists(os.path.dirname(data_output_path)):
#        print(os.path.dirname(data_output_path))
        data_outfile = open( data_output_path , 'a')
    else:
#        print('Failed to find path to data '+ os.path.dirname(data_output_path))
        raise SystemExit('Path to '+data_output_path+' not found')

    ##### Get data from web #####
    if (not is_unit_test):    # Actually attempt to scrape
        content = scraper(url)

        # Check if merge_file is true, then don't add current date to data in output
        if merge_file_test or merge_file_monthly_test:
            data_outfile.write(f'{current_date}_{time_data}: {content}') # All output taken daily, with date/time noted
        else:
            data_outfile.write(f'{time_data}: {content}') # All output recorded on same date and only time noted
    else:
        data_outfile.write(f'Unit test at {time_data} on {current_date}')
    data_outfile.write('\n')
    data_outfile.close()

    return (data_output_path)

def write_data_commodities(url, comm_type, base_folder_path, subfolder_path, csv_list_folder, is_unit_test=False):

    # Get time in HH-MM-SS format
    time_data = strftime('%H:%M:%S',localtime())

    # Get date in YYYY-MM-DD format
    current_date = strftime('%Y-%m-%d')

    # Read in list of commodities from csv file
    comm_folder_path=str(Path().absolute())+'/'+csv_list_folder+'/'
    commodities=csv_reader(comm_folder_path,comm_type)
    # print('Commodities to scrape:',commodities)

    for commodity in commodities.values():
        data_output_path= create_output_filepath(commodity, subfolder_path, base_folder_path, False, True) # Merge monthly
        if is_unit_test:
            print('write_data_comm:',is_unit_test, commodity)

        # Open output file for writing
        try:
            data_outfile = open( data_output_path , 'a')    
            ##### Get data from web #####
            if (not is_unit_test):    # Actually attempt to scrape
                web_content = scraper_comm (url,commodities)
                if commodity in web_content:
                    data_outfile.write(f'{current_date}_{time_data}: {web_content[commodity]}') 
            else:
                data_outfile.write(f'Unit test at {time_data} on {current_date}')
            data_outfile.write('\n')
        except FileNotFoundError as fnf_error:
            print(fnf_error)
        except IOError:
            print("Unable to open "+data_outfile)

        data_outfile.close()

    # return (data_output_path)

##### Create the output file path and filename depending on merge_file flag #####
def create_output_filepath(alt_stock_id,data_subfolder_path,data_folder_base_path,merge_file_test,merge_file_monthly_test,add_year=True,use_filename=True):
    ##### Formatting data file path and filename #####
    # Get date in YYYY-MM-DD format
    current_date = strftime('%Y-%m-%d')
    month_date = strftime('%b-%Y')
    year = strftime('%Y',localtime())
    month = strftime('%B',localtime())

    # Craft base folder path, data path, data subfolder and filename
    base_folder_path = Path.home() / 'Documents'/ 'Code'  # python scraper base path

    # Check if merge_file is true, then add current date to filename
    if use_filename:
        if merge_file_monthly_test:
            file_name = alt_stock_id+'-'+month_date+'.csv'
        elif merge_file_test:
            file_name = alt_stock_id+'.csv'
        else:
            file_name = alt_stock_id+'_'+current_date+'.csv'
            # Merge output path together, sort in folder by year and month
            joined_output_folder_path = os.path.join(base_folder_path,data_folder_base_path,data_subfolder_path,year,month)
    else:
        joined_output_folder_path = os.path.join(base_folder_path,data_folder_base_path,data_subfolder_path,year)

    if any([merge_file_monthly_test, merge_file_test]):
        # Merge output path together, sort in folder by year
        joined_output_folder_path = os.path.join(base_folder_path,data_folder_base_path,data_subfolder_path,year)

    if not add_year:
        joined_output_folder_path = os.path.join(base_folder_path,data_folder_base_path,data_subfolder_path) # no year

    test_path(joined_output_folder_path)
    # print (joined_output_folder_path)
    if not use_filename:
        joined_output = joined_output_folder_path # no file_name
    else:
        joined_output = joinpath(joined_output_folder_path,file_name)
    # print(joined_output)
    return joined_output


##### For Unit testing #####
if (__name__ == '__main__'):    # default to gold as url and stock_name
#    from scrape import bs_scraper as scraper
    # from scrape import bs_scraper_2 as scraper_comm
    # from random_sleep import sleep_time
    from read_csv import csv_reader 

    base_url = 'https://finance.yahoo.com/quote/GC%3DF'
    commodities_url='https://finance.yahoo.com/commodities'
    alt_stock_name = 'Gold'
    merge_file = False     # Expected test case, change to "True" for testing alternative option of one large file
    merge_file_monthly = False     # Expected test case, change to "True" for testing alternative option of one large file per month
    use_year = True
    use_file_name = True
    subfolder_path = 'data'
    csv_list_folder = 'csv_config_files'
    data_folder_output_base_path = 'yahoo-stock-scraper' # folder to put data folder into inside base_folder_path
    unit_test = True     # Disable calls to scrape.py
    csv_base_folder_path=str(Path().absolute())+'/'+csv_list_folder+'/'
    stock_list=csv_reader(csv_base_folder_path, 'fuels')
    stock_type='fuels'

    output_path = create_output_filepath(alt_stock_name,subfolder_path,data_folder_output_base_path,merge_file,merge_file_monthly,use_year,use_file_name)

    write_data(base_url, output_path, merge_file, merge_file_monthly, unit_test)
    write_data_commodities(commodities_url, stock_type, data_folder_output_base_path, subfolder_path, csv_list_folder, unit_test)

    print('Data was written to',output_path)
else:
    from lib.scrape import bs_scraper as scraper # fixes relative path issue when not testing
    from lib.scrape import bs_scraper_2 as scraper_comm 
    from lib.read_csv import csv_reader
