from typing import Text
from selenium import webdriver
from time import sleep
import json
import csv
import datetime
import time

import utils

def crawl_cate_all():
    browser = webdriver.Chrome(executable_path="../chromedriver/chromedriver.exe")
    browser.get("https://www.cophieu68.vn/categorylist.php#")
    cate = browser.find_elements_by_xpath("/html/body/div[7]/table/tbody/tr/td/table[2]/tbody/tr")
    data = []    
    for iter in cate[1:]:
        a = str(iter.text)
        b = a.index("^") 
        c = a[b:] 
        d = c.split(" ")[0]
        e = d.replace("^", "")
        data.append(e)
    dict_cate = {}
    dict_cate["data"] = data
    with open('cate-all.json', 'w') as f:
        json.dump(dict_cate, f)
    print(dict_cate)
    browser.close()

def crawl_cate_stock():
    cate =[]
    f = open('cate-all.json')
    data = json.load(f)   # returns JSON object as a dictionary
    browser = webdriver.Chrome(executable_path="../chromedriver/chromedriver.exe")
    cate_stock_dict ={}
    for cate in data["data"]:   
        browser.get("https://www.cophieu68.vn/categorylist_detail.php?category=^"+ cate)     # nhớ là có cái ^ ở đây 
        com = browser.find_elements_by_xpath("/html/body/table/tbody/tr/td/table[2]/tbody/tr")
        company =[]
        for iter in com[1:]:
            a = str(iter.text)
            b= a.split(" ")[1]
            company.append(str(b))
        cate_stock_dict[cate] = company
    with open('cate-company.json', 'w') as f:
        json.dump(cate_stock_dict, f)
    browser.close()

def crawl_stock_price_v1():

    yesterday = str(datetime.datetime.now() - datetime.timedelta(days=1)).split(" ")[0]
    dir_csv_output = "stock_price_v1/data"
    dir_log_crawl = './stock_price_v1/log_crawl.txt'

    # get day from last time crawl 
    next_day_of_last_time = ''
    with open(dir_log_crawl, 'rt') as f:
        for line in f:
            pass
        last_time_crawl= str(line).split(" ")[0]
        last_time_crawl = datetime.datetime.strptime(last_time_crawl+  ' 1:33PM', '%Y-%m-%d %I:%M%p')
        next_day_of_last_time = str(last_time_crawl + datetime.timedelta(days=1)).split(" ")[0]

    it = 0
    f = open('./cate-company.json')
    data = json.load(f) 
    company_list =[]
    company_err_list =[]

    for key, value in data.items():
        company_list.extend(value)
    
    for row in company_list:
        it = it +1 
        # datetime in yyyy-m-dd format
        loader = utils.DataLoaderVnDirect(symbol= row, start=next_day_of_last_time, end=yesterday)
        try:
            data = loader.download()
            data.to_csv("./"+dir_csv_output+"/"+row+".csv",index=True,mode= 'a',header=False)
            time.sleep(1)
        except:
            company_err_list.append(row)

    with open(dir_log_crawl, 'a') as f:
        f.write('\n{} : crawl from {}, crawl {} company, err len {} err list {} '.format(yesterday,next_day_of_last_time,it,len(company_err_list), company_err_list))
    pass 

if __name__ == "__main__":

    crawl_stock_price_v1()
    # crawl_cate_all()
    #crawl_cate_stock()