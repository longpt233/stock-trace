import monggodb 
from selenium import webdriver
import json 
import time

def crawl():
    list_name = monggodb.get_list_com_name_v1()
    list_name_with_exchange =[]
    for name in list_name: 
        time.sleep(10)
        option = webdriver.ChromeOptions()  
        driver = webdriver.Chrome("../chromedriver/chromedriver.exe",options= option)
        url = "https://finfo-api.vndirect.com.vn/v4/stock_prices?sort=date&size=1&page=1&q=code:" + str(name) 
        print(url)
        driver.get(url=url) 
        ele =driver.find_element_by_css_selector("body > pre")        
        json_raw =  ele.text 
        res = json.loads(json_raw)
        driver.quit()
        data = res["data"][0]["floor"]
        list_name_with_exchange.append({
            name : data
        })

    print(list_name_with_exchange)

if __name__ == "__main__":
    crawl()
    