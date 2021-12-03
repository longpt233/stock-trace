# lam the nao lam co ham sau la dc 

import investpy
import monggodb

# format dd/mm/yyyy
def crawl_one(company,start_day,end_day):
    try:
        data = investpy.get_stock_historical_data(stock=company, country='VietNam', from_date=start_day, to_date=end_day)
        return data
    except:
        print("err at {}".format(company))
        return 0

def crawl_all_company():
    pass

def crawl():
    list_name = monggodb.get_com_name_v2()
    for name in list_name: 
        stock_price_history = monggodb.get_com_price_v2(name)
        # get last 
        last_time_crawl = stock_price_history[data][-1][1] 
        # crawl tu last 

        # append 


    pass 
    