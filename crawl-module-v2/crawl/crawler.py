# lam the nao lam co ham sau la dc 

import datetime
import time
import logging

import utils
import monggodb
import traceback

logging.basicConfig(filename="./crawl.log",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

logger = logging.getLogger('crawl logger')


# format dd/mm/yyyy
def crawl_one(company,start_day,end_day):

    loader = utils.DataLoaderVnDirect(symbol= company, start=start_day, end=end_day)
    data_frame = loader.download()
    time.sleep(1)
    return data_frame    

def crawl_all():
    list_name = monggodb.get_list_com_name_v1()[0:2]
    today = datetime.datetime.today().strftime('%d/%m/%Y')  
    logger.info("start crawl {} company".format(len(list_name)))
    err_list =[]

    for name in list_name: 
        if monggodb.check_exist_stock(name) == False:     # nếu không tồn tại cổ phiếu đó        
            try:
                last_time_crawl = "4/12/2021"   
               
                data_frame = crawl_one(name,last_time_crawl,today)

                data_list =[] 
                for index, rows in data_frame.iterrows(): 
                    my_list =[index, rows.open, rows.high, rows.low, rows.close, rows.volume] 
                    data_list.append(my_list)   

                monggodb.push_com_price_v1_first_time(name,data_list)  # [[Timestamp('2021-12-01 00:00:00'), 36100.0, 36100.0]]
                logger.info("first time crawl {}, numday = {}, from day {}, to day {}".format(name,len(data_list),last_time_crawl, today))
        
            except Exception as e : 
                err_list.append(name)
                logger.error("first time crawl err at {}, err mess {}".format(name,str(e)))
        else:                   
            try: 
                # get last 
                stock_price_history = monggodb.get_com_price_v1(name)
                last_time_crawl = stock_price_history["data"][-1][0]  
                last_time_crawl = last_time_crawl.strftime('%d/%m/%Y')      
                          
                data_frame = crawl_one(name,last_time_crawl,today)
                
                data_list =[] 
                for index, rows in data_frame.iterrows(): 
                    
                    my_list =[index, rows.open, rows.high, rows.low, rows.close, rows.volume] 
                    data_list.append(my_list)   
                
                # push 
                monggodb.push_com_price_v1(name,data_list)  # bo di ngay cu
                logger.info("new time crawl {}, numday = {}, from day {}, to day {}".format(name,len(data_list),last_time_crawl, today))

            except Exception as e :  
                err_list.append(name)
                logger.error("new time crawl err at {}, err mess {}".format(name,str(e)))    
    
    logger.info("total err = {}, list ={}".format(len(err_list), err_list))
    
if __name__ == "__main__":
    crawl_all()