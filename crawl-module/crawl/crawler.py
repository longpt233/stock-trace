from typing import Text
from selenium import webdriver
from time import sleep
import json


def crawl_all_cate():
    browser = webdriver.Chrome(executable_path="../chromedriver/chromedriver_linux")
    browser.get("https://www.cophieu68.vn/categorylist.php#")
    cate = browser.find_elements_by_xpath("/html/body/div[7]/table/tbody/tr/td/table[2]/tbody/tr")
    for iter in cate[1:]:
        a = str(iter.text)
        b = a.index("^") 
        c = a[b:] 
        d = c.split(" ")[0]
        print(d)
    # print(type(cate))   # list
    browser.close()

def crawl_cate_stock():
    cate =[]
    with open('all-cate.txt', 'rt') as f:
        for line in f:
            cate =str(line).split(" ") 
    for i in cate: 
        print("crawl " + i)
        browser = webdriver.Chrome(executable_path="../chromedriver/chromedriver_linux")
        browser.get("https://www.cophieu68.vn/categorylist_detail.php?category="+ i)
        cate = browser.find_elements_by_xpath("/html/body/table/tbody/tr/td/table[2]/tbody/tr")
        company =[]
        for iter in cate[1:]:
            a = str(iter.text)
            b= a.split(" ")[1]
            company.append(str(b))
        with open('all-company.txt', 'a') as f:
            f.write("\""+ i[1:] +"\": "+ str(json.dumps(company)) +",\n")
        browser.close()