from typing import Text
from selenium import webdriver
from time import sleep
import json



cate =[]
with open('all-cate.txt', 'rt') as f:
    for line in f:
        cate =str(line).split(" ") 


for i in cate: 

    print("crawl " + i)
    browser = webdriver.Chrome(executable_path="../../chromedriver/chromedriver_linux")

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