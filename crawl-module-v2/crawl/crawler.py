# lam the nao lam co ham sau la dc 

import monggodb
import datetime
import time 

from typing import Text
from selenium import webdriver
from time import sleep
import json
import csv
import datetime
import time

import utils

# format dd/mm/yyyy
def crawl_one(company,start_day,end_day):
    loader = utils.DataLoaderVnDirect(symbol= company, start=start_day, end=end_day)
    data_frame = loader.download()
    time.sleep(1)
    return data_frame.values.tolist()
    
    

def crawl_all():
    list_name = monggodb.get_list_com_name_v1()[0:1]

    err_list = []
    
    if monggodb.check_collection_empty(): 
        print("FIRST TIME CRAWL")
        
        for name in list_name: 
            try:
                # print("crawl stock :",name)
                time.sleep(10)

                last_time_crawl = "01/01/2015"    # 
                today = datetime.datetime.today().strftime('%d/%m/%Y')   # chi crawl sau 6h toi 
                # today = "02/12/2021" # for test
                data_frame = crawl_one(name,last_time_crawl,today)

                # convert to list
                data_list =[] 
                for index, rows in data_frame.iterrows(): 
                    my_list =[index, rows.Open, rows.High, rows.Low, rows.Close, rows.Volume] 
                    data_list.append(my_list)   

                # push
                monggodb.push_com_price_v1_first_time(name,data_list)  # [[Timestamp('2021-12-01 00:00:00'), 36100.0, 36100.0]]
        
            except: 
                err_list.append(name) 
    else:     
        print("NEW TIME CRAWL")
        
        for name in list_name: 
            try: 
                time.sleep(10)

                # get last 
                stock_price_history = monggodb.get_com_price_v1(name)
                last_time_crawl = stock_price_history["data"][-1][0]  
                last_time_crawl = last_time_crawl.strftime('%d/%m/%Y')      
                
                # crawl tu last toi ngay hom nay
                today = datetime.datetime.today().strftime('%d/%m/%Y')            
                data_frame = crawl_one(name,last_time_crawl,today)
                
                # append , convert to list
                data_list =[] 
                for index, rows in data_frame.iterrows(): 
                    
                    my_list =[index, rows.Open, rows.High, rows.Low, rows.Close, rows.Volume] 
                    data_list.append(my_list)   
                
                # push 
                monggodb.push_com_price_v1(name,data_list[1:])  # bo di ngay cu

            except: 
                err_list.append(name)

    print(err_list)
   
    
    
if __name__ == "__main__":
    crawl_all() 