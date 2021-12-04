import json
import pandas as pd
import sys, getopt, pprint
from pymongo import MongoClient
import csv
import os 

MONGO_URL = "mongodb+srv://longpt:longpt@cluster-longpt.ocem8.mongodb.net/test?authSource=admin&replicaSet=atlas-qdmyf4-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"
myclient = MongoClient(MONGO_URL)
db = myclient["stock_db"]

def push_com_name_v1():
    f = open('./cate-company.json')
    data = json.load(f) 
    company_list =[]
    for key, value in data.items():
        company_list.extend(value)
    company_list = list(set(company_list))

    stock_name_json = {
        "name" :"list company", 
        "data" : company_list
    }

    db["com_name_v1"].insert_one(stock_name_json)
    
    pass  

def push_com_price_v1(): 

    CSV_DATA_PATH = './'
    all_csv_stock_path = [os.path.join(CSV_DATA_PATH, f'{x}') for x in os.listdir(CSV_DATA_PATH)]
    for stock_path  in all_csv_stock_path : 
        results = []
        with open(stock_path) as csvfile:
            reader = csv.reader(csvfile)  
            for row in reader: # each row is a list
                results.append(row)

        name_stock = str(stock_path).split("/")[-1].replace(".csv","")
        a_stock_json = {
            "code" : name_stock,
            "data" : results
        }
        # print(results)
        db["com_price_v1"].insert_one(a_stock_json)


if __name__ == "__main__":

    push_com_name_v1()

