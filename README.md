# yahoo-stock-scraper
Scrapes Yahoo for specified stock and outputs to pre-determined output folder and file name.

By default, if run multiple times during a day, it will concatenate into one file per day.

Add the 
```-m``` 
flag to concatenate data into one file, using the stock name identifier (see examples below).

Add the 
```-v``` 
flag to show version.

Output folder is hard-coded as 
```Data```


## Usage: 
    python3 yahoo-stock-scrapyer.py [Yahoo's URL identifier] [Stock identifier] 

### Examples: 
Executing 

    python3 yahoo-stock-scrapyer.py %E5DJI DJI
Will yield the output filename: 
```DJI_YYYY-MM-DD.csv```

Executing

    python3 yahoo-stock-scrapyer.py GC%3DF Gold

Will yield the output filename: 
```Gold_YYYY-MM-DD.csv```

* Time will be noted with recorded data: 

    ```HH:MM:SS:   0.00 ```

#### **Using the -m flag:**
Executing 

    python3 yahoo-stock-scrapyer.py -m GC%3DF Gold

Will yield the output filename: 
```Gold.csv```

* Date and time will be noted with recorded data: 

    ```YYYY-MM-DD HH:MM:SS:   0.00 ```


### cron job to automate scraper
cron job setting for checking daily (M-F) at 9:00, 9:30, 12:00, 12:30, 16:00, 16:30:
```
 0,30 9,12,16 * * 1-5 /usr/bin/python3 /home/$USER/{folder path}/yahoo-stock-scraper/yahoo-stock-scraper.py GC%3DF Gold 
```
For testing purposes only, DO NOT ABUSE Yahoo's TOS!

## Issues compiling due to importing BeautifulSoup

Issues compiling due to missing bs4 import

``` apt install python3-bs4 ```

## To Do

- ~~Add option to merge into one file~~ (completed)
- ~~Refactor into modular format~~ (completed)
- Add plotting feature
