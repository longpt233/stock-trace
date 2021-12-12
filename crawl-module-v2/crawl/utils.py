from datetime import datetime
import re
from selenium import webdriver
import json
import pandas as pd 

def clean_text(text):
    return re.sub('[(\n\t)*]', '', text).strip()

def convert_date(text, date_type = '%Y-%m-%d'):
    return datetime.strptime(text, date_type)

def convert_text_dateformat(text, origin_type = '%Y-%m-%d', new_type = '%Y-%m-%d'):
    return convert_date(text, origin_type).strftime(new_type)

def split_change_col(text):
    return re.sub(r'[\(|\)%]', '', text).strip().split()

def extract_number(text):
    return int(re.search(r'\d+', text).group(0))


def _isOHLC(data):
    try:
        cols = dict(data.columns)
    except:
        cols = list(data.columns)

    defau_cols = ['high', 'low', 'close', 'open']

    if all(col in cols for col in defau_cols):
        return True
    else:
        return False


def _isOHLCV(data):
    try:
        cols = dict(data.columns)
    except:
        cols = list(data.columns)

    defau_cols = ['high', 'low', 'close', 'open', 'volume']

    if all(col in cols for col in defau_cols):
        return True
    else:
        return False


class  DataLoaderVnDirect():
    def __init__(self, symbol, start, end, *arg, **karg):
        self.symbol = symbol
        self.start = convert_text_dateformat(start, new_type = '%d/%m/%Y')
        self.end = convert_text_dateformat(end, new_type = '%d/%m/%Y') 
        option = webdriver.ChromeOptions() 
        # option.add_argument("--window-size=5,5")
        self.driver = webdriver.Chrome("../chromedriver/chromedriver",options= option)

    def download(self):
        start_date = convert_text_dateformat(self.start, origin_type = '%d/%m/%Y', new_type = '%Y-%m-%d')
        end_date = convert_text_dateformat(self.end, origin_type = '%d/%m/%Y', new_type = '%Y-%m-%d') 
        query = 'code:' + self.symbol
        delta = datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')
        params = {
            "sort": "date",
            "size": delta.days -3,
            "page": 1,
            "q": query,
            "date:gte": start_date,
            "date:lte" : end_date 
        }
 
        url = "https://finfo-api.vndirect.com.vn/v4/stock_prices?sort=date&size="+str(params.get("size"))+"&page=1&q="+str(params.get("q"))+"&date:gte:"+str(params.get("date:gte"))+"&date:lte="+str(params.get("date:lte"))
        print(url)
        self.driver.get(url=url) 
        ele =self.driver.find_element_by_css_selector("body > pre")       
        # print(delta.days) 
        json_raw =  ele.text
        # print(json_raw)
        # json_raw = json_raw[1:]
        # json_raw= json_raw[:-1]

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