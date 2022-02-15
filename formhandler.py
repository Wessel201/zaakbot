# Wessel van Sommeren
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
    for i in range(URLO.code_length()):       
        input_data[i] = f.readline().strip()
    # print(URLO.fields)
    # print(input_data)
    new_u = URLO.NEW_URL
    for num, code in enumerate(URLO.codes):
        new_u += f"entry.{code}={input_data[num]}&"
        
    final = requests.post(new_u[:-1],headers=HEADERS)
    if final.status_code == 200:
        print(f"succesfull posted for:\n\
                Email = {input_data[0]}\n\
                Naam = {input_data[1]}\n\
                Club = {input_data[2]}\n\
                StudieNummer = {input_data[3]}\n\
                Hoeveel = {input_data[4]}")
    else:
        print("failed")
    f.close()

def main(timestring,URL):
    HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
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
    main("00:00:01")