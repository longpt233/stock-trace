import utils
import pandas as pd 
import requests   
import datetime 
from selenium import webdriver

import json

class DataLoaderVnDirect():
    def __init__(self, symbol, start, end, *arg, **karg):
        self.symbol = symbol
        self.start = utils.convert_text_dateformat(start, new_type = '%d/%m/%Y')
        self.end = utils.convert_text_dateformat(end, new_type = '%d/%m/%Y') 
        option = webdriver.ChromeOptions()
        # option.add_argument('headless')
        self.driver = webdriver.Chrome("../../chromedriver/chromedriver_linux",options= option)


    def download(self):
        start_date = utils.convert_text_dateformat(self.start, origin_type = '%d/%m/%Y', new_type = '%Y-%m-%d')
        end_date = utils.convert_text_dateformat(self.end, origin_type = '%d/%m/%Y', new_type = '%Y-%m-%d')
        API_VNDIRECT = 'https://finfo-api.vndirect.com.vn/v4/stock_prices/'
        # query = 'code:' + self.symbol + '~date:gte:' + start_date + '~date:lte:' + end_date
        query = 'code:' + self.symbol
        delta = datetime.datetime.strptime(end_date, '%Y-%m-%d') - datetime.datetime.strptime(start_date, '%Y-%m-%d')
        params = {
            "sort": "date",
            "size": delta.days + 1,
            "page": 1,
            "q": query,
            "date:gte": start_date,
            "date:lte" : end_date 
        }

        # print(params)
        url = "https://finfo-api.vndirect.com.vn/v4/stock_prices?sort=date&size="+str(params.get("size"))+"&page=1&q="+str(params.get("q"))+"&date:gt="+str(params.get("date:gte"))+"&date:lte="+str(params.get("date:lte"))
        
        # print(url)
        # res = requests.get(url="https://finfo-api.vndirect.com.vn/v4/stock_prices?sort=date&size=3994&page=1&q=code:AAM&date:gte=2010-10-10&date:lte=2021-09-15")
        
        res = requests.get(url=url)
        
        # self.driver.get(url=url)
        # # # res = requests.get(url=API_VNDIRECT,params= params)
        # ele =self.driver.find_element_by_css_selector("body > pre")

        # # print(ele.text)

        # res = json.loads(ele.text)

        # self.driver.quit()

        # print(res.text)
        
        data = res.json()["data"]  
        data = pd.DataFrame(data)
        stock_data = data[['date', 'adClose', 'close', 'pctChange', 'average', 'nmVolume',
                        'nmValue', 'ptVolume', 'ptValue', 'open', 'high', 'low']].copy()
        stock_data.columns = ['date', 'adjust', 'close', 'change_perc', 'avg',
                        'volume_match', 'value_match', 'volume_reconcile', 'value_reconcile',
                        'open', 'high', 'low']

        stock_data = stock_data.set_index('date').apply(pd.to_numeric, errors='coerce')
        stock_data.index = list(map(utils.convert_date, stock_data.index))
        stock_data.index.name = 'date'
        stock_data = stock_data.sort_index()
        stock_data.fillna(0, inplace=True)
        stock_data['volume'] = stock_data.volume_match + stock_data.volume_reconcile
  

        return stock_data

import csv

if __name__ == "__main__":
    
    yesterday = str(datetime.datetime.now() - datetime.timedelta(days=1)).split(" ")[0]

    dir_csv = "all"

    next_day_of_last_time = ''
    with open('../../data/vndirect/'+dir_csv+'/1-log-crawl.txt', 'rt') as f:
        for line in f:
            pass
        last_time_crawl= str(line).split(" ")[0]
        last_time_crawl = datetime.datetime.strptime(last_time_crawl+  ' 1:33PM', '%Y-%m-%d %I:%M%p')
        next_day_of_last_time = str(last_time_crawl + datetime.timedelta(days=1)).split(" ")[0]


    it = 0
    with open('../../data/company/company-list.csv', 'rt') as f:
        data = csv.reader(f)
        for row in data:
            # if int(float(row[2]))>10000 and int(float(row[2]))< 30000 :
                it = it +1 
                loader = DataLoaderVnDirect(symbol= row[0], start=next_day_of_last_time, end=yesterday)
                try:
                    data = loader.download()
                    data.to_csv("../../data/vndirect/"+dir_csv+"/"+row[0]+".csv",index=True,mode= 'a',header=False)
                except:
                    print("err at {}".format(row[0]))

    with open('../../data/vndirect/'+dir_csv+'/1-log-crawl.txt', 'a') as f:
        f.write('\n{} : crawl from {}, crawl {} company '.format(yesterday,next_day_of_last_time,it))