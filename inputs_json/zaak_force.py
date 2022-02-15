# Wessel van Sommeren
# Universiteit van Amsterdam 
# wessel.van.sommeren@gmail.com


import requests
import os
import clock
import time
import threading
import json


from datetime import datetime




HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
        

# URL = "https://docs.google.com/forms/d/e/1FAIpQLSfrGn49hcbeioNNa25Osp4fwTG2xV3BmmN9-cMWWC2-xvcQyg/viewform"
URL = "https://docs.google.com/forms/d/e/1FAIpQLScSRgiFy8RnXq714dGeuvtTQJCWFcKyc-ImuEIDA7Tae_rzPg/viewform?usp=sf_link"


class url_obj:
    def __init__(self,URL,headers):
        self.URL = URL
        self.HEADERS = headers
    
        
    def get_codes(self):
        response = requests.get(self.URL,headers = self.HEADERS)
        raw = response.text
        raw2 = raw.split("<script type=\"text/javascript\"")
        for textt in raw2:
            if textt.find("FB_PUBLIC_LOAD_DATA") == -1:
                continue
            result = textt
        results = result.split("[[")[2:]
        self.codes = []
        for res in results:
            try:
                self.codes.append(int(res.split(",")[0]))
            except:
                continue
        self.fields = dict()
        result = result[result.find("FB_PUBLIC_LOAD_DATA_"):]
        # print(result)
        for i in range(len(self.codes)):
            start = result.find('\"') + 1 
            end = result[start:].find('\"')
            term  = result[start:start+end].upper()
            result = result[end+start+1:]
            self.fields[term] = i
            
    def get_new_url(self):
        self.NEW_URL = self.URL[:self.URL.find("viewform")] + "formResponse?"
        
    def code_length(self):
        return len(self.codes)
        

def post_input(filename,URLO):
    f = open(filename,'r')
    input_data = [0 for x in range(URLO.code_length())]
    data = json.loads(f.readline().strip())
    
    
    # for i in range(URLO.code_length()):       
    #     input_data[i] = f.readline().strip()
    # print(URLO.fields)
    for x in data:
        for t in URLO.fields:
            if t.find(x.upper()) != -1:
                flag = 1
                input_data[URLO.fields[t]] = data[x]
                break
    # print(input_data)
    new_u = URLO.NEW_URL
    for num, code in enumerate(URLO.codes):
        new_u += f"entry.{code}={input_data[num]}&"
        
    final = requests.post(new_u[:-1],headers=HEADERS)
    if final.status_code == 200:
        print(f"succesfull posted for:\n\
                Email = {input_data[0]}\n\
                Naam = {input_data[1]}\n\
                Studienummer = {input_data[2]}\n\
                Hoeveelheid = {input_data[3]}")
    else:
        print("failed")
    f.close()

def main(timestring):
    HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    # URL = "https://docs.google.com/forms/d/e/1FAIpQLSeMmB5WuLv9q9UA3WIt2QCZ7ZAdI7f_WxoleOyfGKDN3b9yEw/viewform"
    # # # URL = "https://docs.google.com/forms/d/e/1FAIpQLScSRgiFy8RnXq714dGeuvtTQJCWFcKyc-ImuEIDA7Tae_rzPg/viewform?usp=sf_link"
    # # URL = "https://docs.google.com/forms/d/e/1FAIpQLSe2WQu6a0hSp8yNTRvY7AFsLKzKcr3X2VFklXwnDd0-n4BCxQ/viewform?usp=sf_link"
    
    
    URL = "https://docs.google.com/forms/d/e/1FAIpQLSdnM_R_G1uyLOp2ZC0rJTLILXPC8u87NkRlvyWuG5ICllR_SQ/viewform"
    URLO = url_obj(URL,HEADERS)
    clock.start_clock(timestring)
    URLO.get_codes()
    print(URLO.codes)
    print(URLO.fields)
    URLO.get_new_url()
    for file in os.listdir("inputs"):
        file = "inputs/" + file
        threading.Thread(target = post_input, args = [file,URLO]).start()
    

if __name__ == "__main__":
    main("12:00:01")