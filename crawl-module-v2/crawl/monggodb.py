from pymongo import MongoClient
import csv

MONGO_URL = "mongodb+srv://longpt:longpt@cluster-longpt.ocem8.mongodb.net/test?authSource=admin&replicaSet=atlas-qdmyf4-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true";

def get_list_com_name_v1():
    myclient = MongoClient(MONGO_URL)
    db = myclient["stock_db"]
    collection = db['stock_infor']
    document_dict = collection.find_one({"name":"list all company"})  
    # print(type(document_dict["data"]))  # return list 

    myclient.close()
    return document_dict["data"]


def get_com_price_v1(stock_name):
    myclient = MongoClient(MONGO_URL)
    db = myclient["stock_db"]
    collection = db['stock_price_v1']
    document_dict = collection.find_one({"name":stock_name})  

    myclient.close()
    return document_dict

def push_com_price_v1(stock_name,data_append_list):

    # connect
    myclient_need_close = MongoClient(MONGO_URL)
    db = myclient_need_close["stock_db"]
    collection = db['stock_price_v1']

    # push 
    for data_append in data_append_list:
        collection.update_one({'name': stock_name}, {'$push': {'data': data_append}})

    # close 
    myclient_need_close.close()

def push_com_price_v1_first_time(stock_name,data_first):
    myclient_need_close = MongoClient(MONGO_URL)
    db = myclient_need_close["stock_db"]
    collection = db['stock_price_v1']

    stock_price_json = {
        "name" : stock_name, 
        "data" : data_first   # list
    }
    collection.insert_one(stock_price_json)

    myclient_need_close.close()

def check_exist_stock(stock_name):
    myclient = MongoClient(MONGO_URL)
    db = myclient["stock_db"]
    collection = db['stock_price_v1']

    document_dict = collection.find_one({"name":stock_name}) 

    myclient.close() 
    return document_dict != None

if __name__ == "__main__": 
    print(check_exist_stock("KSV"))

