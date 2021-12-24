import monggodb 
from selenium import webdriver
import json 
import time

CHROME_PATH= "../chromedriver/chromedriver.exe"

# crawl thong tin san giao dich 
def crawl_exchange():
    list_name = monggodb.get_list_com_name_v1()
    list_name_with_exchange =[]
    for name in list_name: 
        time.sleep(10)
        option = webdriver.ChromeOptions()  
        driver = webdriver.Chrome(CHROME_PATH,options= option)
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

# crawl tat ca nhom nganh 
def crawl_cate_all():
    save_json = "./data/cate-all.json"

    browser = webdriver.Chrome(CHROME_PATH)
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
    with open(save_json, 'w') as f:
        json.dump(dict_cate, f)
    print("write to {} ={}".format(save_json,dict_cate))
    browser.close()

def crawl_cate_stock():
    cate =[]
    f = open('./data/cate-all.json')
    data = json.load(f)   # returns JSON object as a dictionary
    browser = webdriver.Chrome(executable_path=CHROME_PATH)
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

if __name__ == "__main__":
    crawl_exchange()
    