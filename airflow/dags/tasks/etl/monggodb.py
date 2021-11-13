from pymongo import MongoClient

MONGO_URL = "mongodb+srv://longpt:longPHan233@cluster-longpt.ocem8.mongodb.net/test?authSource=admin&replicaSet=atlas-qdmyf4-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true";
myclient = MongoClient(MONGO_URL)
db = myclient["stock"]

# all stock_name_v1
def getAllCompany():
    collection = db['stock_name_v1']
    cursor = collection.find({})
    res = []
    
    for document in cursor:  # document is a dict
        res.append({
            "name" : document.get("name"),
            "price":document.get("price")})
 
    return res


def pushAllCompany(listCompany):
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

