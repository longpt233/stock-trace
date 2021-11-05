import json
import pandas as pd
import sys, getopt, pprint
from pymongo import MongoClient

import csv
import os 

IMAGE_PATH = '/home/long/Documents/20211/stock-trace/data/vndirect/all/'
images = [os.path.join(IMAGE_PATH, f'{x}') for x in os.listdir(IMAGE_PATH)]


MONGO_URL = "mongodb+srv://longpt:longPHan233@cluster-longpt.ocem8.mongodb.net/test?authSource=admin&replicaSet=atlas-qdmyf4-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true";
myclient = MongoClient(MONGO_URL)
db = myclient["stock"]

# a_stock_json = {
#     "code" : "A32-NEWFORM",
#     "data" : [{
#         "day" : res[0],
#         "value" : res[1:]
#     }for res in results]
# }



for stock_path  in images : 
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
    db["stock_price_v1"].insert(a_stock_json)