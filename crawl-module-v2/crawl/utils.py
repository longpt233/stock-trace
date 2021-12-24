import datetime 
import re
from selenium import webdriver
import json
import pandas as pd 
import calendar
import requests
from datetime import date
from datetime import timedelta
import time
from bs4 import BeautifulSoup 


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

def crawl_by_thangnch(stock_code):

    to_date = date.today()
    from_date = to_date - timedelta(days=60)

    to_date = to_date.strftime("%Y-%m-%d")
    from_date = from_date.strftime("%Y-%m-%d")
    url = "https://finfo-api.vndirect.com.vn/v4/stock_prices?sort=date&q=code:{}~date:gte:{}~date:lte:{}&size=9990&page=1".format(stock_code, from_date, to_date)
    print(url)
    x = requests.get(url, timeout=10)
    print(x)   # loi khong call ngay dc dau nha 
    json_x = x.json()['data']
    print(json_x)

class DataLoaderCAFE():
    def __init__(self, symbol, start, end, *arg, **karg):
        '''
        %d/%m/%Y format input
        '''
        self.symbol = symbol
        self.start = start
        self.end = end

    def download(self):
        stock_data = pd.DataFrame()

        for i in range(1000):
            stock_slice_batch = self.download_batch(i + 1, self.symbol)
            stock_data = pd.concat([stock_data, stock_slice_batch], axis=0)
            try:
                date_end_batch = stock_slice_batch.date.values[-1]
            except:
                # start date is holiday or weekend
                break
            is_touch_end = convert_date(self.start, '%d/%m/%Y') == convert_date(date_end_batch, '%d/%m/%Y') 
            if is_touch_end:
                break

        return stock_data

    def download_batch(self, id_batch, symbol):
        form_data = {'ctl00$ContentPlaceHolder1$scriptmanager':'ctl00$ContentPlaceHolder1$ctl03$panelAjax|ctl00$ContentPlaceHolder1$ctl03$pager2',
                       'ctl00$ContentPlaceHolder1$ctl03$txtKeyword':symbol,
                       'ctl00$ContentPlaceHolder1$ctl03$dpkTradeDate1$txtDatePicker':self.start,
                       'ctl00$ContentPlaceHolder1$ctl03$dpkTradeDate2$txtDatePicker':self.end,
                       '__EVENTTARGET':'ctl00$ContentPlaceHolder1$ctl03$pager2',
                       '__EVENTARGUMENT':id_batch,
                       '__ASYNCPOST':'true'}
        url = "http://s.cafef.vn/Lich-su-giao-dich-"+symbol+"-1.chn"
        r = requests.post(url, data = form_data, headers = {'content-type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla'}, verify=False)
        soup = BeautifulSoup(r.content, 'html.parser') 
        table = soup.find('table')
        stock_slice_batch = pd.read_html(str(table))[0].iloc[2:, :12] 

        stock_slice_batch.columns = ['date', 'adjust', 'close', 'change_perc', 'avg',
                        'volume_match', 'value_match', 'volume_reconcile', 'value_reconcile',
                        'open', 'high', 'low'] 

        return stock_slice_batch

if __name__ == "__main__":
    # crawl_by_thangnch("ACB")

    # ACB HOSE 
#           date adjust  close      change_perc  avg volume_match   value_match volume_reconcile value_reconcile   open   high    low
# 19  01/12/2021  33.50  33.50    0.20 (0.60 %)  NaN      3620400  120583000000           200000      6220000000  33.10  33.50  33.05

    # AAV HNX 
#           date adjust  close      change_perc  avg volume_match  value_match volume_reconcile value_reconcile   open   high    low
# 19  01/12/2021  26.90  26.90    0.20 (0.75 %)  NaN       652336  17466170200                0               0  26.70   26.7  27.40 

#     01/12/2021	26.90 	26.90 	0.20 (0.75 %)	   	652,336 	17,466,170,200 	0 	0 	                      26.70 	26.7 	27.40 	26.50 
    #


    loader = DataLoaderCAFE(symbol= "AAV", start="01/12/2021", end="24/12/2021")
    # try:
    data = loader.download()
    data = data[::-1]  # start:stop:step. o day -1 tuc la in nguoc 
    print(data)
    # except:
    #     print("err ")