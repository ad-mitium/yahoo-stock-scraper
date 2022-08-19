from .scrape import bs_scraper
from .filepath import outputfilepath
from time import localtime, strftime

if (__name__ == '__main__'):    # for unit testing, default to gold as alt_stock_name
    url_stock_name = 'GC%3DF'
    alt_stock_name = 'Gold'
    merge_file = False
    subfolder_path = 'data/'
    data_folder_base_path = 'yahoo-stock-scraper' # folder to put data folder into inside base_folder_path
    bs_scraper(url_stock_name)
    outputfilepath(alt_stock_name,merge_file,subfolder_path,data_folder_base_path)

def writeout(url_stock_name, alt_stock_name, merge_file, subfolder_path, data_folder_base_path):
    bs_scraper(url_stock_name)
    outputfilepath(alt_stock_name,merge_file,subfolder_path,data_folder_base_path)

    ##### Outputting data to file #####
    # Get time in HH-MM-SS format
    time_data = strftime('%H:%M:%S',localtime()) 

    # Open output file for writing
    output_path = outputfilepath(alt_stock_name,merge_file,subfolder_path,data_folder_base_path)
    data_outfile = open( output_path , 'a')

    content = bs_scraper(url_stock_name)

    # Check if merge_file is true, then don't add current date to data in output
    if merge_file: 
        data_outfile.write(f'{current_date} {time_data}:  {content}') # All output taken daily, with date/time noted
    else:
        data_outfile.write(f'{time_data}:  {content}') # All output recorded on same date and only time noted
    data_outfile.write('\n')
    data_outfile.close()
    return (output_path)


if (__name__ == '__main__'):
    print('Data was written to',writeout(url_stock_name, alt_stock_name, merge_file, subfolder_path, data_folder_base_path))
