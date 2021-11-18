from flask import Flask, render_template
from flask import request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
# import pymongo
import numpy as np
import time
from model import *


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__, template_folder='template')

# way 1
app.config["MONGO_URI"] = "mongodb+srv://readonly:readonly@cluster-longpt.ocem8.mongodb.net/stock"
CORS(app)
mongo = PyMongo(app)
# name_price_collection = mongo.db.lastest_name_price
stock_price_collection = mongo.db.stock_price_v1

chosen_field = [1, 2, 9, 10, 11, 12]  # 'adjust', 'close', 'open', 'high', 'low', 'volume'

# way 2
# myclient = pymongo.MongoClient('mongodb+srv://readonly:readonly@cluster-longpt.ocem8.mongodb.net')
# test = myclient['stock']
# col = test['lastest_name_price']
# print(test.list_collection_names())


@app.route("/data")
def get_data_stock():
    name = request.args.get('code')
    
    stock = stock_price_collection.find_one({'code': name})
    data_stock = stock['data']
    data_stock = list(map(lambda x: [x[i] for i in chosen_field], data_stock))
    data_stock_field = list(map(lambda x: list(map(float, x)), data_stock))

    # find many in mongo
    # output = [{'_id': doc['_id], 'code': doc['code'], 'data': doc['data']} for doc in result]
    # result = jsonify(output)

    return {'data': data_stock_field}


@app.route('/show')
def show():
    return render_template('index.html')


@app.route('/model/predict')
def predict_stock():
    name = request.args.get('code')

    stock = stock_price_collection.find_one({'code': name})
    data_stock = stock['data']
    data_stock = list(map(lambda x: [x[i] for i in chosen_field], data_stock))
    data_stock_field = list(map(lambda x: list(map(float, x)), data_stock))

    try:
        infor = test(name, np.array(data_stock_field))
        return infor
    except:
        return {'message': 'error predict'}


@app.route('/model/train')
def train_model():
    name = request.args.get('code')
    
    stock = stock_price_collection.find_one({'code': name})
    data_stock = stock['data']
    data_stock = list(map(lambda x: [x[i] for i in chosen_field], data_stock))
    data_stock_field = list(map(lambda x: list(map(float, x)), data_stock))

    try:
        train(name, np.array(data_stock_field))
        return {'message': 'done'}
    except:
        return {'message': 'error predict'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
    # get_data_stock()
    # stock = stock_price_collection.find_one({'code': 'SCG'})
    # data_stock = stock['data']
    # data_stock = list(map(lambda x: [x[i] for i in chosen_field], data_stock))
    # data_stock_field = list(map(lambda x: list(map(float, x)), data_stock))
    # train('SCG', np.array(data_stock_field))
    # test('SCG', np.array(data_stock_field))
