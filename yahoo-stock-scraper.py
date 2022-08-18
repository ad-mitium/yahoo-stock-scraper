#!/usr/bin/env python3

# Authored by Timothy Mui 4/22/2022
# Version 0.1.1

# cron job setting for checking daily (M-F) at 9:00, 9:30, 12:00, 12:30, 16:00, 16:30:
# 
# 0,30 9,12,16 * * 1-5 /usr/bin/python3 /home/$USER/{folder path}/yahoo-stock-scraper/yahoo-stock-scraper.py GC%3DF Gold 
# 
# For testing purposes only, DO NOT ABUSE Yahoo's TOS with this!
#
# Issues with BeautifulSoup: apt install python3-bs4

import os
import requests
import argparse
from bs4 import BeautifulSoup
from datetime import datetime,date,time,timezone
from time import localtime, strftime

version_info = (0, 1, 1)
version = '.'.join(str(c) for c in version_info)

# provide description and version info
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description='''
    Scrapes Yahoo for specified stock and outputs to pre-determined output folder and file name. 

    Usage: python3 yahoo-stock-scrapyer.py [Yahoo's URL identifier] [Stock identifier] 
    Example: python3 yahoo-stock-scrapyer.py GC%3DF Gold
                       ''', 
   epilog=' ')
parser.add_argument("url_name", nargs='?', default = 'GC%3DF', help='''Enter stock name for URL''')
parser.add_argument("alt_name", nargs='?', default = 'Gold', help='''Enter common name for stock''')
parser.add_argument('-m','--mergefile', action='store_true', default = False, help='''Merge output into one file''') 
parser.add_argument('-v','--version', action='version', version='%(prog)s {}'.format(version), 
                    help='show the version number and exit')
args = parser.parse_args()

url_stock_name = args.url_name
alt_stock_name = args.alt_name
merge_file = args.mergefile

# Pretend to be Chrome on Windows 10
headers = { 
    'User-Agent'      : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36', 
    'Accept'          : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
    'Accept-Language' : 'en-US,en;q=0.5',
    'DNT'             : '1', # Do Not Track Request Header 
    'Connection'      : 'close'
}

url = 'https://finance.yahoo.com/quote/'+url_stock_name

# Get time in HH-MM-SS format
time_data = strftime('%H:%M:%S',localtime()) 

# Get date in YYYY-MM-DD format
date_data = date.today()
current_date = str(date_data)

# Craft base folder path, data path, data subfolder and filename
user = os.getlogin()
base_folder_path = '/home/'+user+'/Documents/Code/' # python scraper base path
data_folder_base_path = 'yahoo-stock-scraper' # path to put data folder into
subfolder_path = 'data/'

# Check if merge_file is true, then don't add current date to filename
if merge_file: 
    file_name = alt_stock_name+".csv"
else:
    file_name = alt_stock_name+"_"+current_date+".csv"

# Merge output path together before opening file
output_path = os.path.join(base_folder_path,data_folder_base_path,subfolder_path,file_name)
data_outfile = open(output_path, 'a')

# Making a GET request
html_request = requests.get(url, headers=headers, timeout=5)

# Parsing the HTML
soup_output = BeautifulSoup(html_request.content, 'html.parser')

# Find by id
div_id = soup_output.find('div', id= 'quote-header-info')
# Find by class
datafield = div_id.find('fin-streamer', class_= 'Fw(b) Fz(36px) Mb(-4px) D(ib)')
# Get desired content
content = datafield.text.strip()

# Diagnostic output
#print(html_request)
#print(div_id)
#print(merge_file)
#print(datafield)
#print(datafield.text.strip())
#print(output_path)
#print(time_data,":  ",content)
#print(content)
#print(file_name)
#print(current_date)

# Check if merge_file is true, then don't add current date to in data output
if merge_file: 
    data_outfile.write(f"{current_date} {time_data}:  {content}") # All output taken daily, with date/time noted
else:
    data_outfile.write(f"{time_data}:  {content}") # All output recorded on same date and only time noted
data_outfile.write('\n')
data_outfile.close()