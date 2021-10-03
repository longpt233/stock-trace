
import utils
import pandas as pd 
import requests   
import datetime 
from selenium import webdriver
import investpy
import csv


if __name__ == "__main__":
    
    yesterday = str(datetime.datetime.now() - datetime.timedelta(days=1)).split(" ")[0]

    dir_csv = ""

    next_day_of_last_time = ''
    with open('../../data/data-invest/'+dir_csv+'1-log-crawl.txt', 'rt') as f:
        for line in f:
            pass
        last_time_crawl= str(line).split(" ")[0]
        last_time_crawl = datetime.datetime.strptime(last_time_crawl+  ' 1:33PM', '%Y-%m-%d %I:%M%p')
        next_day_of_last_time = str(last_time_crawl + datetime.timedelta(days=1)).split(" ")[0]


    start = '01/06/2009'
    end = datetime.datetime.now().strftime("%d/%m/%Y")

    it = 0
    with open('../../data/company/company-list.csv', 'rt') as f:
        data = csv.reader(f)
        for row in data:
            # if int(float(row[2]))>10000 and int(float(row[2]))< 30000 :
                it = it +1 
                try:
                    data = investpy.get_stock_historical_data(stock=row[0], country='VietNam', from_date=start, to_date=end)
                    data.to_csv("../../data/data-invest/"+dir_csv+row[0]+".csv",index=True,mode= 'a',header=False)
                except:
                    print("err at {}".format(row[0]))

    with open('../../data/data-invest/'+dir_csv+'1-log-crawl.txt', 'a') as f:
        f.write('\n{} : crawl from {}, crawl {} company '.format(yesterday,next_day_of_last_time,it))