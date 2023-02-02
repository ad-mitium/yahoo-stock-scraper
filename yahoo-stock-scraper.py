#!/usr/bin/env python3

# Authored by Timothy Mui 4/22/2022

# For testing purposes only, DO NOT ABUSE Yahoo's TOS with this!
#

import argparse
from lib import writefile
from lib import version as ver

version_number = (0, 4, 1)
subfolder_path = 'data/'
config_folder_path = 'csv_config_files/'
data_folder_output_base_path = 'yahoo-stock-scraper' # folder to put data folder into inside base_folder_path: ~/Documents/Code

##### Command line interaction for user supplied variables #####
# provide description and version info
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description='''
    Scrapes Yahoo for specified stock and outputs to pre-determined output folder and file name. 

    Usage: python3 yahoo-stock-scrapyer.py [Yahoo's URL identifier] [Stock identifier] 
    Example: python3 yahoo-stock-scrapyer.py GC%3DF Gold
                       ''', 
   epilog=' ')
#parser.add_argument("url_name", nargs='?', default = 'GC%3DF', help='''Enter stock name for URL''')
#parser.add_argument("alt_name", nargs='?', default = 'Gold', help='''Enter common name for stock''')
parser.add_argument('url_div_id_name', help='''Enter stock name for URL''')
parser.add_argument('alt_stock_id_name', help='''Enter common name for stock''')
parser.add_argument('-c','--comm-type', action='store_true', default = False, help='''enable commodities scraping''') 
parser.add_argument('-f','--fuels', action='store_true', default = False, help='''select fuel commodities''') 
parser.add_argument('-i','--indexes', action='store_true', default = False, help='''select indexes''') 
parser.add_argument('-p','--precious-metals', action='store_true', default = False, help='''select precious metals commodities''') 
parser.add_argument('-o','--other', action='store_true', default = False, help='''select custom list of commodities''') 
parser.add_argument('-m','--mergefile-large', action='store_true', default = False, help='''merge data output into one file''') 
parser.add_argument('-mo','--mergefile-monthly', action='store_true', default = False, help='''merge data output into one monthly file''') 
parser.add_argument('-v','--version', action='version', version='%(prog)s {}'.format(ver.ver_info(version_number)), 
                    help='show the version number and exit')
args = parser.parse_args()

url_stock_name = args.url_div_id_name
alt_stock_name = args.alt_stock_id_name
merge_file = args.mergefile_large
merge_file_monthly = args.mergefile_monthly

base_url = 'https://finance.yahoo.com/quote/'+url_stock_name

output_path = writefile.create_output_filepath(alt_stock_name,subfolder_path,data_folder_output_base_path,merge_file,merge_file_monthly)

# Read in commodity types for scraping 
if args.comm_type:
    commodities_url='https://finance.yahoo.com/commodities'

    # print('Commdities enabled\n', end='')
    if args.fuels:
        commodity_type='fuels'
    elif args.precious_metals:
        commodity_type='precious_metals'
    elif args.indexes:
        commodity_type='indexes'
    elif args.other:
        commodity_type='other'
    else:
        commodity_type='indexes'
        print('Defaulted to indexes.\n', end='')

    writefile.write_data_commodities(commodities_url,commodity_type, data_folder_output_base_path, subfolder_path, config_folder_path)
else:
    data_to_file = writefile.write_data(base_url, output_path, merge_file, merge_file_monthly) 
