# lam the nao lam co ham sau la dc 

import investpy
import monggodb
import datetime
import time
import traceback

# format dd/mm/yyyy
def crawl_one(company,start_day,end_day):
    try:
        data = investpy.get_stock_historical_data(stock=company, country='VietNam', from_date=start_day, to_date=end_day)  # startday < enday, return >= 2 day  
        return data
    except:
        # print("ERR CRAWL AT {}".format(company))
        return None

def crawl_all():

    print("crawl all starting")


    list_name = monggodb.get_com_name_v2()

    err_list = []
    
    if monggodb.check_collection_empty(): 
        print("FIRST TIME CRAWL")
        
        for name in list_name: 
            try:
                # print("crawl stock :",name)
                time.sleep(10)

                last_time_crawl = "01/01/2015"    # 
                today = datetime.datetime.today().strftime('%d/%m/%Y')   # chi crawl sau 6h toi 
                # today = "02/12/2021" # for test
                data_frame = crawl_one(name,last_time_crawl,today)

                # convert to list
                data_list =[] 
                for index, rows in data_frame.iterrows(): 
                    my_list =[index, rows.Open, rows.High, rows.Low, rows.Close, rows.Volume] 
                    data_list.append(my_list)   

                # push
                monggodb.push_com_price_v2_first_time(name,data_list)  # [[Timestamp('2021-12-01 00:00:00'), 36100.0, 36100.0]]
        
            except:
                # print("CATCH ERR AT " + name )
                err_list.append(name)
                # print(traceback.format_exc())
    else:     
        print("NEW TIME CRAWL")
        
        for name in list_name[0:2]: 
            try:
                # print("crawl stock :",name)
                time.sleep(10)

                # get last 
                stock_price_history = monggodb.get_com_price_v2(name)
                last_time_crawl = stock_price_history["data"][-1][0]            # datetime.datetime 
                # last_time_crawl = last_time_crawl + datetime.timedelta(days=1)  # crawl tu ngay tiep theo  . 
                # update : investpy phai crawl toi thieu 2 ngay => ti cai list bo di ngay nay cx dc 
                last_time_crawl = last_time_crawl.strftime('%d/%m/%Y')          # chuan hao ve dung dinh dang
                
                # crawl tu last toi ngay hom nay
                today = datetime.datetime.today().strftime('%d/%m/%Y')            
                data_frame = crawl_one(name,last_time_crawl,today)
                
                # append , convert to list
                data_list =[] 
                for index, rows in data_frame.iterrows(): 
                    
                    my_list =[index, rows.Open, rows.High, rows.Low, rows.Close, rows.Volume] 
                    data_list.append(my_list)   
                
                # push 
                monggodb.push_com_price_v2(name,data_list[1:])  # bo di ngay cu

            except:
                # print("CATCH ERR AT " + name )
                # print(traceback.format_exc())
                err_list.append(name)

    print(err_list)
   
    
    
if __name__ == "__main__":
    crawl_all() 