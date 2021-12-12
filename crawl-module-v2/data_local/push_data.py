import json
import pandas as pd
import sys, getopt, pprint
from pymongo import MongoClient
import csv
import os 


MONGO_URL = "mongodb+srv://longpt:longpt@cluster-longpt.ocem8.mongodb.net/test?authSource=admin&replicaSet=atlas-qdmyf4-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"
myclient = MongoClient(MONGO_URL)
db = myclient["stock_db"]


def push_com_name_all():

    f = open('./cate-company.json')
    data = json.load(f) 
    company_list =[]
    for key, value in data.items():
        company_list.extend(value)
    company_list = list(set(company_list))

    stock_name_json = {
        "name" :"list all company", 
        "data" : company_list,
        "length" : len(company_list)
    }

    db["stock_infor"].insert_one(stock_name_json)
    
    pass  

def push_cate_name_all():

    cate_list =[]
    f = open('cate-all.json')
    data = json.load(f)
    for cate_iter in data["data"]: 
        cate_list.append(cate_iter)

    stock_name_json = {
        "name" :"list all cate", 
        "data" : cate_list,
        "length" : len(cate_list)
    }

    db["stock_infor"].insert_one(stock_name_json)
    
    pass  


def push_cate_with_all_stock():

    f = open('./cate-company.json')
    data = json.load(f)  

    stock_name_json = {
        "name" :"list all cate with stock", 
        "data" : data
    }

    db["stock_infor"].insert_one(stock_name_json)
    
    pass  


if __name__ == "__main__":
    # push_com_name_all()
    # push_cate_name_all()
    push_cate_with_all_stock()