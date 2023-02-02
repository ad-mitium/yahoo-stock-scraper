#!/usr/bin/env python3

import csv


def csv_reader(folder_path,comm_type,unit_test=False):
    d={}
    csv_file=comm_type
    infile=str(folder_path)+csv_file+'.csv'
    # print(infile)
    try:
        with open(infile, newline='') as csv_input_file:
            csv_data = csv.DictReader(csv_input_file)
            d=create_dict_from_csv(csv_data)    
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except IOError:
        print("Unable to load "+infile)
    return d

def create_dict_from_csv(csv_data, unit_test=False):

    stock_name_dict={}

    for row in csv_data:
        # print (row)
        stock_name_dict=row.copy()
    
    # print("Stock_list: "+str(stock_name_dict))

    return stock_name_dict

    ##### For Unit testing #####
if (__name__ == '__main__'):    #
    from pathlib import Path
    
    subfolder_path = 'csv_config_files'
    data_folder_output_base_path = 'yahoo-stock-scraper' # folder to put data folder into inside base_folder_path
    unit_test = True     # 

    base_folder_path=str(Path().absolute())+'/'+subfolder_path+'/'
    csv_indexes='indexes'
    csv_precious_metals='precious_metals'
    csv_fuels='fuels'

    indexes=csv_reader(base_folder_path,csv_indexes,unit_test)
    precious_metals=csv_reader(base_folder_path,csv_precious_metals,unit_test)
    fuels=csv_reader(base_folder_path,csv_fuels,unit_test)

    print ("index: "+str(indexes),"\nprecious_metals: "+str(precious_metals),"\nfuels: "+str(fuels))
else:
    print('', end='')
