import os
from pathlib import Path
from time import localtime, strftime


def write_error_data(data_output_path, content, insert_time=True, is_unit_test=False):

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

    if insert_time:
        data_outfile.write(f'{current_date}_{time_data} {content}\n') # All output taken daily, with date/time noted
    else:
        data_outfile.write(f'    {content}\n') # All output taken daily, with date/time noted
        
    # data_outfile.write('\n')
    data_outfile.close()

    return (data_output_path)

def create_instant_filename(prefix):
    ##### Formatting data file path and filename #####
    # Get date in YYYY-MM-DD format
    current_date = strftime('%Y-%m-%d')
    month_date = strftime('%b-%Y')
    year = strftime('%Y',localtime())
    month = strftime('%B',localtime())
    
    #print (type(prefix))
    
    if not prefix == None:
        filename = prefix+'_'+current_date+'.csv'
    else:
        filename = current_date+'.csv'

    print(filename)
    return (filename)

def create_output_filepath(data_subfolder_path,data_folder_base_path,filename,add_year=True,use_filename=True,is_unit_test=False):
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
        file_name = filename+'_'+current_date+'.csv'
        #file_name = filename+'_'+current_date+'.csv'
        # Merge output path together, sort in folder by year and month
        joined_output_folder_path = os.path.join(base_folder_path,data_folder_base_path,data_subfolder_path,year,month)
    else:
        joined_output_folder_path = os.path.join(base_folder_path,data_folder_base_path,data_subfolder_path,year)

    if not add_year:
        joined_output_folder_path = os.path.join(base_folder_path,data_folder_base_path,data_subfolder_path) # no year

    test_path(joined_output_folder_path)
    # print (joined_output_folder_path)
    if not use_filename:
        joined_output = joined_output_folder_path # no file_name
    else:
        joined_output = joinpath(joined_output_folder_path,file_name)
    #if is_unit_test:
        #print(joined_output)
    return joined_output


##### For Unit testing #####
if (__name__ == '__main__'):    # default to gold as url and stock_name
    import common
    
    use_timestamp = True
    use_year = True             # Create year directory, allows for checking csv_config folder
    use_file_name = True        # Useful for creating and testing folders, allows for checking csv_config folder
    subfolder_path = 'data'     # Folder name to store created debug file
    data_folder_output_base_path = 'yahoo-stock-scraper' # folder to put data folder into inside base_folder_path
    unit_test = True     
    filename = 'yahoo_stock_error'
    
    error_data = "Data is put here"

    output_path = create_output_filepath(subfolder_path,data_folder_output_base_path,filename,use_year,use_file_name)

    write_error_data(output_path, error_data, use_timestamp, unit_test)

    print('Data was written to',output_path)
    
    print(create_instant_filename('None'))
else:
    from lib.common import test_path
    from lib.common import joinpath
    
    print()
