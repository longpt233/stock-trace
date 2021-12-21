import datetime 
import re
from selenium import webdriver
import json
import pandas as pd 
import calendar


def convert_date(text, date_type = '%Y-%m-%d'):
    return datetime.datetime.strptime(text, date_type)

def convert_text_dateformat(text, origin_type = '%Y-%m-%d', new_type = '%Y-%m-%d'):
    return convert_date(text, origin_type).strftime(new_type)


def normal_day_count(start, end):
    '''
    tính từ  (start, end ]
    neu start = end thi tra ve 0 
    '''
    start_date  = datetime.datetime.strptime(start, '%d/%m/%Y')
    end_date    = datetime.datetime.strptime(end, '%d/%m/%Y')
    num = 0 
    for i in range((end_date - start_date).days):
        day       = calendar.day_name[(start_date + datetime.timedelta(days=i+1)).weekday()]
        if day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            num= num +1 
    return num

class  DataLoaderVnDirect():
    
    def __init__(self, symbol, start, end):
        '''
        %d/%m/%Y format input
        '''
        self.symbol = symbol
        self.start = start
        self.end = end
        option = webdriver.ChromeOptions()  
        self.driver = webdriver.Chrome("../chromedriver/chromedriver",options= option)

    def download(self):
        
        numday_need_crawl = normal_day_count(self.start, self.end)
 
        url = "https://finfo-api.vndirect.com.vn/v4/stock_prices?sort=date&size="+str(numday_need_crawl)+"&page=1&q=code:" + str(self.symbol) 
        print(url)
        self.driver.get(url=url) 
        ele =self.driver.find_element_by_css_selector("body > pre")        
        json_raw =  ele.text 

        res = json.loads(json_raw)

        self.driver.quit()

        data = res["data"]  
        data = pd.DataFrame(data)
        stock_data = data[['date', 'adClose', 'close', 'pctChange', 'average', 'nmVolume',
                        'nmValue', 'ptVolume', 'ptValue', 'open', 'high', 'low']].copy()
        stock_data.columns = ['date', 'adjust', 'close', 'change_perc', 'avg',
                        'volume_match', 'value_match', 'volume_reconcile', 'value_reconcile',
                        'open', 'high', 'low']

        stock_data = stock_data.set_index('date').apply(pd.to_numeric, errors='coerce')
        stock_data.index = list(map(convert_date, stock_data.index))
        stock_data.index.name = 'date'
        stock_data = stock_data.sort_index()
        stock_data.fillna(0, inplace=True)
        stock_data['volume'] = stock_data.volume_match + stock_data.volume_reconcile

        return stock_data