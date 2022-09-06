import requests
from bs4 import BeautifulSoup

# Issues with BeautifulSoup: apt install python3-bs4


def bs_scraper(url):

    ##### Scraping info #####

    # Pretend to be Chrome on Windows 10
    headers = { 
        'User-Agent'      : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36', 
        'Accept'          : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
        'Accept-Language' : 'en-US,en;q=0.5',
        'DNT'             : '1', # Do Not Track Request Header 
        'Connection'      : 'close'
    }

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
    return content

if (__name__ == '__main__'):    # for unit testing, default to gold as url_stock_name
    url = 'https://finance.yahoo.com/quote/GC%3DF'
    print(bs_scraper(url))