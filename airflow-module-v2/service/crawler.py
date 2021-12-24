# lam the nao lam co ham sau la dc 
 
import monggodb
import datetime
import time 
import utils

# format dd/mm/yyyy tra ve [] vi du 01/12  -> tra tu 01/12
def crawl_one(company,start_day,end_day,dict_name_exchange):

    exchange = dict_name_exchange[company]

    loader = utils.DataLoaderCAFE(symbol= company, start=start_day, end=end_day, exchange=exchange) 
    data_frame = loader.download()
    time.sleep(2) 
    return data_frame  

def crawl_all():

    print("crawl all starting") 

    dict_name_exchange = monggodb.get_name_exchange()

    err_list = []
    
    list_name = monggodb.get_list_com_name_v1()
    today = datetime.datetime.today().strftime('%d/%m/%Y')    
    err_list =[]

    for name in list_name[:2]: 
        if monggodb.check_exist_stock(name) == False:     # nếu không tồn tại cổ phiếu đó        
            try:
                last_time_crawl = "01/01/2015"   
               
                data_frame = crawl_one(name,last_time_crawl,today,dict_name_exchange)

                data_list =[] 
                for index, rows in data_frame.iterrows(): 
                    my_list =[rows.date, rows.open, rows.high, rows.low, rows.close, rows.volume] 
                    data_list.append(my_list)   

                monggodb.push_com_price_v1_first_time(name,data_list[::-1]) # cai list nay bi nguoc vcl 
                print("first time crawl {}, numday = {}, from day {}, to day {}".format(name,len(data_list),last_time_crawl, today))
        
            except Exception as e : 
                err_list.append(name)
        else:                   
            try: 
                # get last 
                stock_price_history = monggodb.get_com_price_v1(name) 
                last_time_crawl = stock_price_history["data"][-1][0]        
                          
                data_frame = crawl_one(name,last_time_crawl,today,dict_name_exchange)
                
                data_list =[] 
                for index, rows in data_frame.iterrows(): 
                    
                    my_list =[rows.date, rows.open, rows.high, rows.low, rows.close, rows.volume] 
                    data_list.append(my_list)   
                
                # push 
                monggodb.push_com_price_v1(name,data_list[::-1][1:])  # lay 1 vi ham crwa crawl thua cai dau 
                
            except Exception as e :  
                err_list.append(name)  
    
    print("total err = {}, list ={}".format(len(err_list), err_list))
   
    
    
if __name__ == "__main__":

    crawl_all()