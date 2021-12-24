from pymongo import MongoClient
import json
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

    # close 
    myclient_need_close.close()

def push_com_price_v1_first_time(stock_name,data_first):
    myclient_need_close = MongoClient(MONGO_URL)
    db = myclient_need_close[db_name]
    collection = db['stock_price_v1']

    stock_price_json = {
        "name" : stock_name, 
        "data" : data_first   # list
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


def push_com_name_all():

    myclient = MongoClient(MONGO_URL)
    db = myclient[db_name]

    f = open('./data/cate-company.json')
    data = json.load(f) 
    company_list =[]
    for key, value in data.items():
        company_list.extend(value)
    company_list = list(set(company_list))

    stock_name_json = {
        "name" :"name_all", 
        "description" :"danh sach tat ca cac cong ty",
        "data" : company_list,
        "length" : len(company_list)
    }

    db["stock_info"].insert_one(stock_name_json)
    myclient.close() 
    pass  

def push_cate_name_all():
    myclient = MongoClient(MONGO_URL)
    db = myclient[db_name]

    cate_list =[]
    f = open('./data/cate-all.json')
    data = json.load(f)
    for cate_iter in data["data"]: 
        cate_list.append(cate_iter)

    stock_name_json = {
        "name" :"cate_all", 
        "description" :"danh sach tat ca cac nhom nganh",
        "data" : cate_list,
        "length" : len(cate_list)
    }

    db["stock_info"].insert_one(stock_name_json)
    myclient.close() 
    pass  


def push_cate_with_all_stock():
    myclient = MongoClient(MONGO_URL)
    db = myclient[db_name]

    f = open('./data/cate-company.json')
    data = json.load(f)  

    stock_name_json = {
        "name" :"cate_name", 
        "description" :"danh sach cac cong ty trong nhom nganh",
        "data" : data
    }

    db["stock_info"].insert_one(stock_name_json)
    myclient.close() 
    pass  

def push_name_and_exchange_all():
    myclient = MongoClient(MONGO_URL)
    db = myclient[db_name]
 
    f = open('./data/exchange-all.json')
    data = json.load(f) 

    stock_name_json = {
        "name" :"exchange_all", 
        "description" :"danh sach tat ca cac cong ty cung san giao dich",
        "data" : data["data"],
        "length" : len(data["data"])
    }

    db["stock_info"].insert_one(stock_name_json)
    myclient.close() 
    pass  


def push_name_and_exchange_revert_all():
    myclient = MongoClient(MONGO_URL)
    db = myclient[db_name]
 
    f = open('./data/exchange-all.json')
    data = json.load(f) 

    dict_exchange={
        "HOSE":[],
        "UPCOM":[],
        "HNX":[]
    }

    for name_exchange in data["data"]:
        for key, value in name_exchange.items():
            if "HOSE" == value:
                dict_exchange["HOSE"].append(key)
            if "HNX" == value:
                dict_exchange["HNX"].append(key)
            if "UPCOM" == value:
                dict_exchange["UPCOM"].append(key)
    

    stock_json = {
        "name" :"exchange_revert", 
        "description" :"danh sach cac san giao dich va cong ty trong do",
        "data" : dict_exchange
    }

    db["stock_info"].insert_one(stock_json)
    myclient.close() 
    pass  

    

