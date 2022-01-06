from time import time
from datetime import datetime
from pymongo import MongoClient
import config


MONGO_URL = config.MONGO_URL

db_name = "stock_trace"

def get_list_com_name_v1():
    print(MONGO_URL)
    myclient = MongoClient(MONGO_URL)
    db = myclient[db_name]
    collection = db['stock_info']
    document_dict = collection.find_one({"name":"name_all"})   

    myclient.close()
    return document_dict["data"]

def get_com_price_v1(stock_name):
    myclient = MongoClient(MONGO_URL)
    db = myclient[db_name]
    collection = db['stock_price_v1']
    document_dict = collection.find_one({"name":stock_name})  

    myclient.close()
    return document_dict

def push_com_price_v1(stock_name,data_append_list):

    # connect
    myclient_need_close = MongoClient(MONGO_URL)
    db = myclient_need_close[db_name]
    collection = db['stock_price_v1']

    # push 
    for data_append in data_append_list:
        print("append to stock",stock_name," value= ", data_append)
        collection.update_one({'name': stock_name}, {'$push': {'data': data_append}})
        
    collection.update_one({'name': stock_name}, {'$set':{"last-update": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}})

    # close 
    myclient_need_close.close()

def push_com_price_v1_first_time(stock_name,data_first):
    myclient_need_close = MongoClient(MONGO_URL)
    db = myclient_need_close[db_name]
    collection = db['stock_price_v1']

    stock_price_json = {
        "name" : stock_name, 
        "data" : data_first,   # list
        "last-update": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    collection.insert_one(stock_price_json)

    myclient_need_close.close()

def check_exist_stock(stock_name):
    myclient = MongoClient(MONGO_URL)
    db = myclient[db_name]
    collection = db['stock_price_v1']

    document_dict = collection.find_one({"name":stock_name}) 

    myclient.close() 
    return document_dict != None

def get_name_exchange():

    myclient = MongoClient(MONGO_URL)
    db = myclient[db_name]
    collection = db['stock_info']
    list_obj_document = collection.find_one({"name":"exchange_all"})   

    myclient.close()
    dict_exchange={
    }

    for name_exchange in list_obj_document["data"]:
        for key, value in name_exchange.items():
            dict_exchange[key]=value


    return dict_exchange
  