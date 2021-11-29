from pymongo import MongoClient

MONGO_URL = "mongodb+srv://longpt:longpt@cluster-longpt.ocem8.mongodb.net/test?authSource=admin&replicaSet=atlas-qdmyf4-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true";
myclient = MongoClient(MONGO_URL)
db = myclient["stock"]


def get_all_company_v1():

    collection = db['stock_name_v1']
    all_document = collection.find({})     # get all document 

    list_name_price = []
    
    for dict_document in all_document:           # document is a dict
        list_name_price.append({        
            "name" : dict_document.get("name"),
            "price": dict_document.get("price")
        })
 
    return list_name_price


def get_all_company_v2():

    collection = db['stock_name_v2']
    all_document = collection.find({})     # get all document 

    list_name_price = []
    
    for dict_document in all_document:           # document is a dict
        list_name_price.append({        
            "name" : dict_document.get("name"),
            "price": dict_document.get("price")
        })
 
    return list_name_price

def push_all_company_v1(list_company_price):
    pass

def push_all_company_v2(list_company_price):

    
    pass

# minimize stock_name_v2
def getTargetCompany():
    return


def pushTargetCompany():
    return


def getAllCompanyAndPrice():
    pass


def pushAllCompanyAndPrice():
    pass

