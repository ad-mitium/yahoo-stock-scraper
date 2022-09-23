import requests
from bs4 import BeautifulSoup as bSoup

# Issues with BeautifulSoup: apt install python3-bs4

def get_page(url_to_scrape):

    # Pretend to be Chrome on Windows 10
    headers = { 
        'User-Agent'      : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.125 Safari/537.36', 
        'Accept'          : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
        'Accept-Language' : 'en-US,en;q=0.5',
        'DNT'             : '1', # Do Not Track Request Header 
        'Connection'      : 'close'
    }

    # Making a GET request
    html_request = requests.get(url_to_scrape, headers=headers, timeout=10)
    return (html_request)

##### Scraping info #####
def bs_scraper(url_to_scrape, is_unit_test=False):
    if not is_unit_test:
        sleep_time(20) # Randomly sleep to increase variability

    web_request = get_page(url_to_scrape)

    # Parsing the HTML
    soup_html_output = bSoup(web_request.content, 'html.parser')

    # Find by id
    div_id = soup_html_output.find('div', id= 'quote-header-info')
    # Find by class
    datafield = div_id.find('fin-streamer', class_= 'Fw(b) Fz(36px) Mb(-4px) D(ib)')
    # Get desired content
    content = datafield.text.strip()
    return content

if (__name__ == '__main__'):    # for unit testing, default to gold as url_stock_name
    from random_sleep import sleep_time
    unit_test=True
    base_url = 'https://finance.yahoo.com/quote/GC%3DF'
    print(bs_scraper(base_url,unit_test))
else:
    from lib.random_sleep import sleep_time
    
    print()
