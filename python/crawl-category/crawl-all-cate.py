from typing import Text
from selenium import webdriver
from time import sleep

browser = webdriver.Chrome(executable_path="../../chromedriver/chromedriver_linux")

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