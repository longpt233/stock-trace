# stock-trace
craw, analyze, predict  
## Structure Data 

- một số file cần chú ý

```
crawl     
|--airflow-module-v2: lập lịch crawl giá   
|   |-- service 
|         |-- config.py : đạt config monggo atlas tại đây 
|         |-- crawler.py : crawl giá của tất cả công ti có trong document `name_all` được đẩy từ crawler_infor.py bên dưới
|       
|--crawl-module-v2: crawl các thông tin liên quan cổ phiếu
|   |-- crawl : 
|         |-- data: kết quả crawl thôn tin   
|         |-- crawler_infor.py: crawl thông tin + đẩy lên monggo 
|         |-- config.py : đạt config monggo atlas tại đây 
|   |-- crawl_article: crawl báo liên quan chứng khoán 
|
|--ETL_EDA: chứa các EDA dữ liệu
|
|--Model_demo: các thử nghiệm về model, độ đo , feature 
|   |-- final.ipynb : một số điều chỉnh về feature, độ đo
|
|--visualize: backend+ frontend

```

## Read data
```python 

MONGO_URL = "mongodb+srv://readonly:readonly@longpt-cluster.ufbfx.mongodb.net/test"
import pymongo
def get_his_by_name(stock_name): 
    myclient = pymongo.MongoClient(MONGO_URL)
    db = myclient["stock_trace"]
    collection = db['stock_price_v1']
    document_dict = collection.find_one({"name":stock_name})    
    myclient.close()
    return document_dict["data"]

stock_name = "ACB"
numpy_array = np.array(get_his_by_name(stock_name))
df[stock_name] = pd.DataFrame(numpy_array, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
```

## How to run 
- chạy crawl-module > airflow 
- chi tiết xem trong readme của module tương ứng

## Note 
- config với user rw bất đắc dĩ phải public lên, mong là k ai vô xóa database :< 
