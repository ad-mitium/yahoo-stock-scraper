import requests
from bs4 import BeautifulSoup as bSoup

error_filename_prefix = 'error_message_logging'
app_name = 'yahoo-stock-scraper'
subfolder_path = 'data'     # Folder name to store created debug file

# Issues with BeautifulSoup: apt install python3-bs4

def read_data(filename):
    data_infile = open( filename , 'r')
    read_data=data_infile.read()
    data_infile.close()
    return read_data

def get_page(url_to_scrape, is_unit_test=False):

    # Pretend to be Chrome on Windows 10
    headers = {
        'User-Agent'      : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept'          : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language' : 'en-US,en;q=0.5',
        'DNT'             : '1', # Do Not Track Request Header
        'Connection'      : 'close'
    }
    if is_unit_test:
        from pathlib import Path
        stock='GC%3DF'
        sample_data=str(Path().absolute())+'/sample_data/yahoo-sample.html'
        sample_data_single=str(Path().absolute())+'/sample_data/yahoo-sample-single.html'
        print('  get_page data:',sample_data)
        print('  get_page unit test:',is_unit_test)

    # Making a GET request
    try:
        if is_unit_test:
            print('  try get data:',is_unit_test)
            if stock in url_to_scrape:
                html_request = read_data(sample_data_single)
            else:
                html_request = read_data(sample_data)
            return (html_request)
        else:
            html_request = requests.get(url_to_scrape, headers=headers, timeout=10)
            if html_request.status_code == 200:
                if is_unit_test:
                    print('  Success:',html_request.status_code)
                return (html_request)
            html_request.raise_for_status()
    except requests.exceptions.Timeout as e_t:
        if is_unit_test:
            print('  A timeout error has occurred getting page with error message: \n',e_t)
        return ("A timeout exception has occurred:" + repr(e_t))
    except requests.exceptions.RequestException as e:
        if is_unit_test:
            print('  An error has occurred getting page with error message: \n', e)
        return ("An exception has occurred: \n" + repr(e))

##### Scraping info #####
def bs_scraper(url_to_scrape, is_unit_test=False):
    if is_unit_test:
        print("bs_scraper:",is_unit_test)
    if not is_unit_test:
        sleep_time(10) # Randomly sleep to increase variability
        web_request = get_page(url_to_scrape)
        # Parsing the HTML
        soup_html_output = bSoup(web_request.content, 'html.parser')
    else:
        web_request = get_page(url_to_scrape,is_unit_test)
        # Parsing the HTML
        soup_html_output = bSoup(web_request, 'html.parser')

    if "exception has occurred:" not in soup_html_output:
        # Find by id
        if is_unit_test and soup_html_output.find('div', id= 'svelte'):
            print('    svelte div found')
        elif is_unit_test:
            print('    svelte div not found')
        div_id = soup_html_output.find('div', id= 'svelte')
        # Find by class
        fin_streamer = div_id.find('fin-streamer', class_= 'livePrice') 
        retry_count=0
        while retry_count < 10:
            if not hasattr(fin_streamer,'data-field'):  # Try a second time
                print ("Trying again")
                web_request = get_page(url_to_scrape)
                # Parsing the HTML
                soup_html_output = bSoup(web_request.content, 'html.parser')
                div_id = soup_html_output.find('div', id= 'svelte')
                fin_streamer = div_id.find('fin-streamer', class_= 'livePrice') 
                retry_count += 1
                sleep_time(3) # Randomly sleep to increase variability because Yahoo is actively blocking repeated requests
            else:
                break
            
        # Data is found, time to extract data
        if hasattr(fin_streamer,'data-field'): 
        #if fin_streamer.has_attr('data-field'): 
            if fin_streamer['data-field'] == 'regularMarketPrice':  # Check if data exists
                datafield = fin_streamer
                if is_unit_test:
                    print('regularMarketPrice found')
                    print('    fin-streamer data: ',fin_streamer)     # Dump div data for assessment
                #write_error_data(create_output_filepath(subfolder_path,app_name,error_filename_prefix,True,True),fin_streamer)
            else:
                datafield = fin_streamer
                if is_unit_test:
                    print('regularMarketPrice NOT found')
                    print('    fin-streamer data: ',fin_streamer)     # Dump div data for assessment
                write_error_data(create_output_filepath(subfolder_path,app_name,error_filename_prefix,True,True),div_id.find('fin-streamer'))

            # Get desired content
            try:
                if is_unit_test:
                    print('    try text strip')
                content = datafield.text.strip()
            except AttributeError:
                
                content = "No Data Acquired"
                if is_unit_test:
                    print('    fin-streamer data: ',fin_streamer)     # Dump div data for assessment
                write_error_data(create_output_filepath(subfolder_path,app_name,error_filename_prefix,True,True),div_id.find('fin-streamer'))

                # Alert on lack of data
                #play()
        else:       # Catchall for data NoneType found
            #if is_unit_test:
            print('NoneType found')
            print('    fin-streamer data: ',fin_streamer)     # Dump div data for assessment
            content = 'Scrape Failed -> NoneType found'
            #content = ' Scrape failed because fin-streamer not found'  # send exception alert as data
            write_error_data(create_output_filepath(subfolder_path,app_name,error_filename_prefix,True,True),div_id.find('fin-streamer'))

            # Implement error logging for troubleshooting
            import re
            write_error_data(create_output_filepath(subfolder_path,app_name,error_filename_prefix,True,True),'###############################################################')     # Add separator line to make log easier to read

            for fin_test_data in div_id.find_all(re.compile('fin-streamer')):   # Dump all fin-streamer data for review
                #print(fin_test_data)
                write_error_data(create_output_filepath(subfolder_path,app_name,error_filename_prefix,True,True),fin_test_data,False) # Don't print timestamp
                if 'regularMarketPrice' and 'livePrice' in str(fin_test_data):
                    #print(fin_test_data)
                    write_error_data(create_output_filepath(subfolder_path,app_name,error_filename_prefix,True,True),fin_test_data)
            write_error_data(create_output_filepath(subfolder_path,app_name,error_filename_prefix,True,True),'###############################################################')     # Add separator line to make log easier to read

    else:
        content = soup_html_output   # send exception as data
        write_error_data(create_output_filepath(subfolder_path,app_name,error_filename_prefix,True,True),div_id.find('fin-streamer'))
    return content

def bs_scraper_2(url_to_scrape, stock_name_data, is_unit_test=False):
    d={}
    if is_unit_test:
        print("bs_scraper_2:",is_unit_test)

    # Parsing the HTML
    if not is_unit_test:
        web_request = get_page(url_to_scrape)
        soup_html_output = bSoup(web_request.content, 'html.parser')
    else:
        web_request = get_page(url_to_scrape,is_unit_test)
        soup_html_output = bSoup(web_request, 'html.parser')

    if "exception has occurred:" not in soup_html_output:
        # Find by id
        if is_unit_test:
           print('  No exceptions found')

        div_id = soup_html_output.find('div', id= 'svelte')
        if is_unit_test:
            print('  svelte divs')
            # print (div_id)

        div_ids=div_id.find_all("fin-streamer")
        if is_unit_test:
            print ('  fin-streamer divs')
            # print (div_ids)

        for divs in div_ids:
            if divs.has_attr('data-symbol'):
                data_symbol=divs['data-symbol']
                # if is_unit_test:
                #     print('    ',data_symbol)
            if divs.has_attr('data-field'):
                data_type=divs['data-field']
            for stock_name in stock_name_data.keys():
                if data_symbol==stock_name and data_type=='regularMarketPrice':
                    if stock_name in stock_name_data.keys():
                        stock_name=stock_name_data[stock_name]
                    if is_unit_test:
                        print('    Trying text strip')
                    try:
                        d[stock_name] = divs.text.strip()
                    except AttributeError:
                
                        d[stock_name] = "No Data Acquired"
                        if is_unit_test:
                            print('    div data: ',divs)     # Dump div data for assessment
                        #error_filename = write_error.create_instant_filename(filename)
                        write_error.write_error_data(write_error.create_output_filepath(subfolder_path,app_name,error_filename_prefix,True,True),divs)
                    #except e:
                        # Alert on lack of data
                        #play()

                    if is_unit_test:
                        print('     ',stock_name, end=' = ')
                        print (divs.text.strip())
        if is_unit_test:
            print("  Found:",d)
        content = d
    else:
        content = soup_html_output   # send exception as data
    return content

if (__name__ == '__main__'):    # for unit testing, default to gold as url_stock_name
    from random_sleep import sleep_time
    from pathlib import Path
    import write_error
    #from play_audio import play_audio as play
    
    unit_test=True
    folder_output_base_path = 'yahoo-stock-scraper' # folder to put data folder into inside base_folder_path
    stock='GC%3DF'
    # stock='NG%3DF'
    stock_alt_names={'GC=F':'Gold', 'CL=F':'Crude', '^DJI':'DJIA', '^IXIC':'NASDAQ', 'NG=F':'NG', 'RB=F':'Gas' }

    # You must do this unit test from the base folder path (<Location this code repo is stored> / folder_output_base_path)
    # Sample data is hosted in another github repo and must be placed in the main folder of this repo
    sample_data=str(Path().absolute())+'/sample_data/yahoo-sample.html' # This is only used for unit test, so Path.absolute shouldn't be an issue
    sample_data_single=str(Path().absolute())+'/sample_data/yahoo-sample-single.html'

    base_url = 'https://finance.yahoo.com/quote/'+str(stock)
    base_url_com = 'https://finance.yahoo.com/commodities'
    
    print('bs_scraper_2 Returned: ',bs_scraper_2(base_url_com,stock_alt_names,unit_test))
    print('bs_scraper Returned: ',bs_scraper(base_url,unit_test))

    data_folder_output_base_path = 'yahoo-stock-scraper' # folder to put data folder into inside base_folder_path
    filename = 'yahoo_error_message'

else:
    from lib.random_sleep import sleep_time
    #from lib.play_audio import play_audio as play
    from lib.write_error import create_output_filepath 
    from lib.write_error import write_error_data
    
    print()
