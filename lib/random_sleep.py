from random import randint
from time import sleep, strftime

def sleep_time(n):
    start_time = int(strftime('%S'))
    rand_time=randint(1,n)
    stop_time = start_time+a
    
    current_time = start_time

    if printout:
        print('Sleeping for',rand_time,'seconds. Starting at',start_time,'Stopping at',stop_time)
    
    while current_time <= stop_time:
        sleep(1)
    
        if printout:
            remaining = '{:2d}'.format(stop_time - current_time)
            print (remaining,end='\r')
        current_time += 1

if (__name__ == '__main__'):    # for unit testing
    printout = True

    sleep_time(10)
    print(f'\r') # Don't write over final number printed out for remaining
else:
    printout = False