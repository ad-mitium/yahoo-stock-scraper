#!/usr/bin/env python3
# 
import os
from pathlib import Path
from time import localtime, strftime

def test_path(output_folder_path):
    if os.path.exists(output_folder_path):
        # print(os.path.dirname(output_folder_path))
        pass
    else:
        print('Failed to find path to data '+ os.path(output_folder_path),'\n    Creating missing folders')
        Path(output_folder_path).mkdir( parents=True, exist_ok=True)
        # raise SystemExit('Path to '+output_folder_path+' not found')

def joinpath(rootdir, targetdir):
    return os.path.join(os.sep, rootdir + os.sep, targetdir)


###### Create the output file path and filename only #####
def create_output_filepath(data_subfolder_path,data_folder_base_path,filename,add_year=True,use_filename=True,is_unit_test=False):
    ##### Formatting data file path and filename #####
    # Get date in YYYY-MM-DD format
    current_date = strftime('%Y-%m-%d')
    year = strftime('%Y',localtime())
    month = strftime('%B',localtime())

    # Craft base folder path, data path, data subfolder and filename
    base_folder_path = Path.home() / 'Documents'/ 'Code'  # python scraper base path

    # Check if merge_file is true, then add current date to filename
    if use_filename:
        file_name = filename+'_'+current_date+'.csv'

        # Merge output path together, sort in folder by year and month
        joined_output_folder_path = os.path.join(base_folder_path,data_folder_base_path,data_subfolder_path,year,month)
    else:
        # Merge output path together, sort in folder by year
        joined_output_folder_path = os.path.join(base_folder_path,data_folder_base_path,data_subfolder_path,year)

    if not add_year:
        joined_output_folder_path = os.path.join(base_folder_path,data_folder_base_path,data_subfolder_path) # no year

    # Check if folder path exists and create folder path if it doesn't
    test_path(joined_output_folder_path)
    #if is_unit_test: 
        #print (joined_output_folder_path)
    
    if not use_filename:
        joined_output = joined_output_folder_path # no file_name
    else:
        joined_output = joinpath(joined_output_folder_path,file_name)
    #if is_unit_test:
        #print(joined_output)
    return joined_output

###### Create the output file path and using stock name as filename depending on merge_file flag #####
def create_stock_output_filepath(alt_stock_id,data_subfolder_path,data_folder_base_path,merge_file_test,merge_file_monthly_test,add_year=True,use_filename=True):
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
        # Merge output path together, sort in folder by year
        joined_output_folder_path = os.path.join(base_folder_path,data_folder_base_path,data_subfolder_path,year)

    if any([merge_file_monthly_test, merge_file_test]):
        # Merge output path together, sort in folder by year
        joined_output_folder_path = os.path.join(base_folder_path,data_folder_base_path,data_subfolder_path,year)

    if not add_year:
        joined_output_folder_path = os.path.join(base_folder_path,data_folder_base_path,data_subfolder_path) # no year

    # Check if folder path exists and create folder path if it doesn't
    test_path(joined_output_folder_path)
    #if is_unit_test: 
        #print (joined_output_folder_path)

    if not use_filename:
        joined_output = joined_output_folder_path # no file_name
    else:
        joined_output = joinpath(joined_output_folder_path,file_name)
    # print(joined_output)
    return joined_output

