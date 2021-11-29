# lam the nao lam co ham sau la dc 

import investpy

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


def crawl_all_cate():
    
    pass
    