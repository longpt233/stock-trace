import csv 
from bs4 import BeautifulSoup 
import requests
import utils
import pandas as pd 
import requests   
import datetime

class DataLoaderCAFE():
    def __init__(self, symbol, start, end, *arg, **karg):
        self.symbol = symbol
        self.start = utils.convert_text_dateformat(start, new_type = '%d/%m/%Y')
        self.end = utils.convert_text_dateformat(end, new_type = '%d/%m/%Y') 

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
            is_touch_end = utils.convert_date(self.start, '%d/%m/%Y') == utils.convert_date(date_end_batch, '%d/%m/%Y') 
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

        print(stock_slice_batch)

        stock_slice_batch.columns = ['date', 'adjust', 'close', 'change_perc', 'avg',
                        'volume_match', 'value_match', 'volume_reconcile', 'value_reconcile',
                        'open', 'high', 'low'] 

        return stock_slice_batch


if __name__ == "__main__":

    
    yesterday = str(datetime.datetime.now() - datetime.timedelta(days=1)).split(" ")[0]

    next_day_of_last_time = ''
    with open('../../data/csv-10-30/1-log-crawl.txt', 'rt') as f:
        for line in f:
            pass
        last_time_crawl= str(line).split(" ")[0]
        last_time_crawl = datetime.datetime.strptime(last_time_crawl+  ' 1:33PM', '%Y-%m-%d %I:%M%p')
        next_day_of_last_time = str(last_time_crawl + datetime.timedelta(days=1)).split(" ")[0]


    it = 0
    with open('../../data/company/company-list.csv', 'rt') as f:
        data = csv.reader(f)
        for row in data:
            if int(float(row[2]))>10000 and int(float(row[2]))< 30000 :
                it = it +1 
                loader = DataLoaderCAFE(symbol= row[0], start=next_day_of_last_time, end=yesterday)
                try:
                    data = loader.download()[::-1] # to revert 
                    data.to_csv("../../data/csv-10-30/"+row[0]+".csv",index=False,mode= 'a',header=False)
                except:
                    print("err at {}".format(row[0]))

    with open('../../data/csv-10-30/1-log-crawl.txt', 'a') as f:
        f.write('\n{} : crawl from {}, crawl {} company '.format(yesterday,next_day_of_last_time,it))