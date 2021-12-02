import json
import pandas as pd
import sys, getopt, pprint
from pymongo import MongoClient

import csv
import os 

CSV_DATA_PATH = './'
all_csv_stock_path = [os.path.join(CSV_DATA_PATH, f'{x}') for x in os.listdir(CSV_DATA_PATH)]

MONGO_URL = "mongodb+srv://longpt:lonpt@cluster-longpt.ocem8.mongodb.net/test?authSource=admin&replicaSet=atlas-qdmyf4-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"
myclient = MongoClient(MONGO_URL)
db = myclient["stock_db"]

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
    db["com_name_v1"].insert(a_stock_json)