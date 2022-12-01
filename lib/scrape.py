import requests
from bs4 import BeautifulSoup as bSoup

# Issues with BeautifulSoup: apt install python3-bs4

def get_page(url_to_scrape, is_unit_test=False):

    # Pretend to be Chrome on Windows 10
    headers = { 
        'User-Agent'      : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.71 Safari/537.36', 
        'Accept'          : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
        'Accept-Language' : 'en-US,en;q=0.5',
        'DNT'             : '1', # Do Not Track Request Header 
        'Connection'      : 'close'
    }
    if is_unit_test:
        print('get_page unit test:',is_unit_test)

    # Making a GET request
    try:
        html_request = requests.get(url_to_scrape, headers=headers, timeout=10)
        if html_request.status_code == 200:
            if is_unit_test:
                print('Success:',html_request.status_code)
            return (html_request)
        html_request.raise_for_status()
    except requests.exceptions.Timeout() as e_t:
        if is_unit_test:
            print('A timeout error has occurred getting page with error message: \n',e_t)
        return "A timeout exception has occurred:" + repr(e_t)
#        raise SystemExit(e)
    except requests.exceptions.RequestException as e:
        if is_unit_test:
            print('An error has occurred getting page with error message: \n', e)
#        raise SystemExit(e)
        return "An exception has occurred: \n" + repr(e)

##### Scraping info #####
def bs_scraper(url_to_scrape, is_unit_test=False):
 #   print(is_unit_test)
    if not is_unit_test:
        sleep_time(20) # Randomly sleep to increase variability
        web_request = get_page(url_to_scrape)
    else:
        web_request = get_page(url_to_scrape,is_unit_test)

    
    # Parsing the HTML
    soup_html_output = bSoup(web_request.content, 'html.parser')

    if "exception has occurred:" not in soup_html_output:
        # Find by id
        div_id = soup_html_output.find('div', id= 'quote-header-info')
        # Find by class
        datafield = div_id.find('fin-streamer', class_= 'Fw(b) Fz(36px) Mb(-4px) D(ib)')
        # Get desired content
        content = datafield.text.strip()
    else:
        content = soup_html_output   # send exception as data
    return content

if (__name__ == '__main__'):    # for unit testing, default to gold as url_stock_name
    from random_sleep import sleep_time
    unit_test=True
    base_url = 'https://finance.yahoo.com/quote/GC%3DF'

    print('Returned: ',bs_scraper(base_url,unit_test))
else:
    from lib.random_sleep import sleep_time
    
    print()
