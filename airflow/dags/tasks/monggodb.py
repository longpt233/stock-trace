from pymongo import MongoClient
import csv

MONGO_URL = "mongodb+srv://longpt:longpt@cluster-longpt.ocem8.mongodb.net/test?authSource=admin&replicaSet=atlas-qdmyf4-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true";
myclient = MongoClient(MONGO_URL)
db = myclient["stock_db"]

def get_com_name_v2():
    collection = db['com_name_v2']
    all_document = collection.find({})     # get all document 
    list_name = []
    for dict_document in all_document:           # document is a dict
        list_name.append(dict_document.get("data"))
    return list_name

def push_com_name_v2(name, data):
    stock_name_json = {
        "name" : name, 
        "data" : data   # list
    }
    db["com_name_v2"].insert_one(stock_name_json)

def get_com_price_v2(stock_name):
    collection = db['com_price_v2']
    document_dict = collection.find_one({"name":stock_name})  
    return document_dict

def push_com_price_v2(stock_name,data_append):
    collection = db['com_price_v2']
    collection.update_one({'name': stock_name}, {'$push': {'data': data_append}})


if __name__ == "__main__":
    # push_com_name_v2()
    # dict = get_com_price_v2("ACB")
    push_com_price_v2("ACB", 10)

