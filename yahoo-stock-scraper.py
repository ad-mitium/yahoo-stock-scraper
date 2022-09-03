#!/usr/bin/env python3

# Authored by Timothy Mui 4/22/2022

# For testing purposes only, DO NOT ABUSE Yahoo's TOS with this!
#

import argparse
from lib import writefile
from lib import version as ver

version_number = (0, 2, 1)
version = ver.ver_info(version_number)
subfolder_path = 'data/'
data_folder_base_path = 'yahoo-stock-scraper' # folder to put data folder into inside base_folder_path: ~/Documents/Code

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
parser.add_argument('alt_id_name', help='''Enter common name for stock''')
parser.add_argument('-m','--mergefile', action='store_true', default = False, help='''merge data output into one file''') 
parser.add_argument('-v','--version', action='version', version='%(prog)s {}'.format(ver.ver_info(version_info)), 
                    help='show the version number and exit')
args = parser.parse_args()

url_stock_name = args.url_div_id_name
alt_stock_name = args.alt_id_name
merge_file = args.mergefile

data_to_file = writefile.writeout(url_stock_name, alt_stock_name, merge_file, subfolder_path, data_folder_base_path)
