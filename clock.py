# Wessel van Sommeren
import time 
from datetime import datetime




def start_clock(timestring):
    date_format = "%H:%M:%S"
    a = datetime.strptime(timestring, date_format)

    while True:
        b = datetime.strptime(datetime.now().strftime("%H:%M:%S"), date_format)
        delta  = a - b
        second = delta.total_seconds()
        if second < 0: 
            break
        else:
            print("              ", end = "\r")
            print(f" {second} seconds till launch" ,end="\r")
            time.sleep(1)
