from pymongo import MongoClient
import csv

MONGO_URL = "mongodb+srv://longpt:longpt@cluster-longpt.ocem8.mongodb.net/test?authSource=admin&replicaSet=atlas-qdmyf4-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true";
myclient = MongoClient(MONGO_URL)
db = myclient["stock_db"]

def get_com_name_v2():

    collection = db['com_name_v2']
    all_document = collection.find({})     # get all document 

    list_name_price = []
    
    for dict_document in all_document:           # document is a dict
        list_name_price.append(dict_document.get("data"))
 
    return list_name_price

def push_com_name_v2():

    filename ="./com_name_v2.csv"
    rows =[]
    with open(filename, 'r') as csvfile: 
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)   # extracting field names through first row
        for row in csvreader:      # extracting each data row one by one
            rows.append(row[1])

    stock_name_json = {
        "name" :"list company 20-35 ", 
        "data" : rows
    }

    db["com_name_v2"].insert_one(stock_name_json)


if __name__ == "__main__":

    # push_com_name_v2()
    print(get_com_name_v2())
