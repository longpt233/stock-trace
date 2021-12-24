import datetime 
import pandas as pd 
import requests
from bs4 import BeautifulSoup 


def convert_date(text, date_type = '%Y-%m-%d'):
    return datetime.datetime.strptime(text, date_type)

def convert_text_dateformat(text, origin_type = '%Y-%m-%d', new_type = '%Y-%m-%d'):
    return convert_date(text, origin_type).strftime(new_type)


class DataLoaderCAFE():
    def __init__(self, symbol, start, end,exchange):
        '''
        %d/%m/%Y format input
        '''
        self.exchange= exchange
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

        if self.exchange == "UPCOM":
            stock_slice_batch = pd.read_html(str(table))[0].iloc[2:, :15] 

            stock_slice_batch.columns = ['date', 'adjust', 'close','gia binh quan', 'change_perc', 'avg',
                            'volume_match', 'value_match', 'volume_reconcile', 'value_reconcile', 'gia tham chieu',
                            'open', 'high', 'low'] 

        if self.exchange == "HOSE":
            stock_slice_batch = pd.read_html(str(table))[0].iloc[2:, :12] 

            stock_slice_batch.columns = ['date', 'adjust', 'close', 'change_perc', 'avg',
                            'volume_match', 'value_match', 'volume_reconcile', 'value_reconcile',
                            'open', 'high', 'low'] 
        
        if self.exchange == "HNX":
            stock_slice_batch = pd.read_html(str(table))[0].iloc[2:, :13] 

            stock_slice_batch.columns = ['date', 'adjust', 'close', 'change_perc', 'avg',
                            'volume_match', 'value_match', 'volume_reconcile', 'value_reconcile','gia tham chieu',
                            'open', 'high', 'low'] 
        
        stock_slice_batch['volume'] = stock_slice_batch.volume_match + stock_slice_batch.volume_reconcile

        return stock_slice_batch


