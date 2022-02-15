# Wessel van Sommeren
# Universiteit van Amsterdam 
# wessel.van.sommeren@gmail.com


import time 
import requests
import formhandler
import clock

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

START_TIME = "12:29:00"


# URL = "https://docs.google.com/forms/d/e/1FAIpQLSdnM_R_G1uyLOp2ZC0rJTLILXPC8u87NkRlvyWuG5ICllR_SQ/viewform"

URL = "https://docs.google.com/forms/d/e/1FAIpQLSeMmB5WuLv9q9UA3WIt2QCZ7ZAdI7f_WxoleOyfGKDN3b9yEw/viewform?usp=sf_link"

clock.start_clock(START_TIME)

while True:
    response = requests.get(URL,headers=HEADERS)
    if response.text.find("FB_PUBLIC_LOAD_DATA_") != -1:
        print("form is open")
        break
    else:
        time.sleep(1)
        print("form is closed")

formhandler.main("00:00:01",URL)