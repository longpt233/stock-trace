#install nếu chưa install
#pip install dnspython

"""#Tien xu ly du lieu co phieu

  - Loc nhung co phieu co volume nho
  - Loc nhung co phieu co gia mua outlier
"""

#Import thu vien
import numpy as np
import pandas as pd
import datetime
import ast
from datetime import datetime as dt
from datetime import date, timedelta

import pymongo
from pymongo import MongoClient

#Doc du lieu
#Doc data tu file csv
# stock_price = pd.read_csv('/content/drive/MyDrive/stock_price_v1.csv', encoding="utf_8")
# stock_price

#Xu lu du lieu
# #Moi ma CP duoc tach thanh 1 DataFrame rieng
# DF_list = list()
# for i in range(0,965):
#   new_data = pd.DataFrame(columns=['_id','code','data'])
#   new_data.loc[0] = stock_price.loc[i]

#   #Bo cot '_id'
#   new_data = new_data.drop(columns=['_id'])
#   DF_list.append(new_data)


# #Xu ly voi moi ma CP _ cho file local, csv
# '''
#   data_of_stock: Chuoi du lieu cua CP
#   period_long : Do dai ngay lay mau, mac dinh bang 30
#   Ham se tinh tu ngay cuoi cung crawl data den het period_long
# '''
# def data_convert(data_of_stock, period_long=30):
#   #Chuyen kieu data_of_stock tu string thanh list
#   #tmp_data = []
#   tmp_data = ast.literal_eval(data_of_stock)
#   tmp_df_price = pd.DataFrame(tmp_data, columns=['Date', 'Adjust', 'Close', 'Change_perc',\
#                                                  'Avg', 'Volume_match', 'Value_match', 'Volume_recolcile',\
#                                                  'Value_reconcile', 'Open', 'High', 'Low', 'Volume'])
#   #Bo nhung truong du lieu khong can thiet
#   tmp_df_price = tmp_df_price.drop(columns=['Adjust', 'Change_perc', 'Avg', 'Value_match', \
#                                             'Volume_recolcile', 'Value_reconcile',\
#                                             'Open', 'High', 'Low','Volume'])
#   #Chuyen date thanh dang chuan datetime
#   tmp_df_price['Date'] = pd.to_datetime(tmp_df_price['Date']).dt.date

#   #Chon khoang thoi gian de xet 
#   days_before = (tmp_df_price['Date'].max()-timedelta(days=period_long)).isoformat()
#   new_day = dt.strptime(days_before, '%Y-%m-%d').date()
  
#   #Tach khoang thoi gian xet thanh 1 DataFrame moi
#   new_df = tmp_df_price.loc[(tmp_df_price['Date']>=new_day) &\
#                             (tmp_df_price['Date']<=tmp_df_price['Date'].max())]
  
#   #Dat Date lam index
#   df_0 = new_df
#   df_0 = df_0.set_index('Date')

#   #Bo sung nhung ngay con thieu trong khoang thoi gian tren
#   idx = pd.date_range(df_0.index.min(), df_0.index.max())

#   df_0.index = pd.DatetimeIndex(df_0.index)
#   df_0 = df_0.reindex(idx)
#   #Nhung ngay missing value se duoc dien nhu sau: 
#   # - Close: bang gia cua ngay lien truoc
#   # - Volume_match: bang 0
#   df_0.loc[:,['Close']] = df_0.loc[:,['Close']].ffill()
#   df_0['Volume_match'] = df_0['Volume_match'].fillna(value=0)
  
#   #Them cot 'Check_volume_per_day', co gia tri = 1, neu Volume > 0 (= 0, neu nguoc lai)
#   default_check = [0 for x in range(0, len(df_0))]
#   for i in range(0, len(df_0)):
#     if(float(df_0['Volume_match'][i]) != 0):
#       default_check[i] = 1
#   df_0['Check_volume_per_day'] = default_check

#   return df_0

#Xu ly voi moi ma CP _ cho file online tren mongodb
'''
  data_of_stock: Chuoi du lieu cua CP
  period_long : Do dai ngay lay mau, mac dinh bang 30
  Ham se tinh tu ngay cuoi cung crawl data den het period_long
'''
def data_convert_mongo(data_of_stock, period_long=30):

  tmp_data = data_of_stock
  tmp_df_price = pd.DataFrame(tmp_data, columns=['Date', 'Adjust', 'Close', 'Change_perc',\
                                                 'Avg', 'Volume_match', 'Value_match', 'Volume_recolcile',\
                                                 'Value_reconcile', 'Open', 'High', 'Low', 'Volume'])
  #Bo nhung truong du lieu khong can thiet
  tmp_df_price = tmp_df_price.drop(columns=['Adjust', 'Change_perc', 'Avg', 'Value_match', \
                                            'Volume_recolcile', 'Value_reconcile',\
                                            'Open', 'High', 'Low','Volume'])
  #Chuyen date thanh dang chuan datetime
  tmp_df_price['Date'] = pd.to_datetime(tmp_df_price['Date']).dt.date

  #Chon khoang thoi gian de xet 
  days_before = (tmp_df_price['Date'].max()-timedelta(days=period_long)).isoformat()
  new_day = dt.strptime(days_before, '%Y-%m-%d').date()
  
  #Tach khoang thoi gian xet thanh 1 DataFrame moi
  new_df = tmp_df_price.loc[(tmp_df_price['Date']>=new_day) &\
                            (tmp_df_price['Date']<=tmp_df_price['Date'].max())]
  
  #Dat Date lam index
  df_0 = new_df
  df_0 = df_0.set_index('Date')

  #Bo sung nhung ngay con thieu trong khoang thoi gian tren
  idx = pd.date_range(df_0.index.min(), df_0.index.max())

  df_0.index = pd.DatetimeIndex(df_0.index)
  df_0 = df_0.reindex(idx)
  #Nhung ngay missing value se duoc dien nhu sau: 
  # - Close: bang gia cua ngay lien truoc
  # - Volume_match: bang 0
  df_0.loc[:,['Close']] = df_0.loc[:,['Close']].ffill()
  df_0['Volume_match'] = df_0['Volume_match'].fillna(value=0)
  
  #Them cot 'Check_volume_per_day', co gia tri = 1, neu Volume > 0 (= 0, neu nguoc lai)
  default_check = [0 for x in range(0, len(df_0))]
  for i in range(0, len(df_0)):
    if(float(df_0['Volume_match'][i]) != 0):
      default_check[i] = 1
  df_0['Check_volume_per_day'] = default_check

  return df_0

#Cac ham loc co phieu theo gia tham chieu va khoi luong GD

#Loc co phieu trong khoang gia (min,max)
#Tra ve 0 neu ma bi loai
'''
  min_price: muc gia thap nhat
  max_price: muc gia cao nhat
'''
def check_by_price(data_frame,min_price=20.0, max_price=35.0):
  sum_price = data_frame['Close'].apply(lambda x: float(x))
  mean_price = sum_price.mean()

  #check = 0
  if ((mean_price >= min_price) & (mean_price <= max_price)):
    check = 1
    #print('Ma CP thoa man')
  else:
    check = 0
    #print('Ma CP khong thoa man')
  
  return mean_price, check

#Loc co phieu co volume bat thuong
#Xet theo tuan, neu co >= 50% so tuan co muc volume khong dat ==> Loai (return 0)
#Moi tuan, neu co <= 40% so ngay co muc volume khong dat ==> Loai
def check_by_volume(data_frame):
  check = 0
  data_frame = data_frame.reset_index()
  data_frame = data_frame.rename(columns={"index": "Date"})
  data_frame['Date'] = pd.to_datetime(data_frame['Date']).dt.date

  #Tach cac ngay cua tuan gan nhat ra khoi dataframe (vi co the co it hon 7 ngay)
  latest_day = data_frame['Date'].max()
  idx = (latest_day.weekday() + 1) % 7 # MON = 0, SUN = 6 -> SUN = 0 .. SAT = 6
  latest_sunday = latest_day - datetime.timedelta(7+idx-6 - 1) 

  t1_new = data_frame.loc[(data_frame['Date'] >= data_frame['Date'].min()) & \
                          (data_frame['Date'] <= latest_sunday)]
  t2_new = data_frame.loc[(data_frame['Date'] > latest_sunday) & \
                          (data_frame['Date'] <= data_frame['Date'].max())]

  #Xet t1_new
  t1_new['Date'] = pd.to_datetime(t1_new['Date'])
  t1 = t1_new.groupby(pd.Grouper(key="Date", freq="W")).sum()
  t1['Probality'] = t1['Check_volume_per_day'] / 5
  count = 0
  for i in range(0, len(t1)):
    if t1['Probality'][i]<=0.4:
      count = count + 1

  #Xet t2_new
  a = t2_new['Date'].max().weekday()
  if (a <= 4): #la ngay trong tuan
    w_2 = t2_new['Check_volume_per_day'].sum() / len(t2_new)
  else: #la ngay cuoi tuan
    w_2 = t2_new['Check_volume_per_day'].sum() / 5

  if w_2 <= 0.4:
    count = count + 1

  w = count/(len(t1)+1)
  if w < 0.5:
    check = 1
    #print('Chap nhan duoc')
  
  return check

# #Dung cho file csv tren local
# def filter_stock(data, minPrice=20.0, maxPrice=35.0, periodLong=30):
#   #Tao dataframe luu tat ca cac ma CP va cac gia tri can loc
#   main_df = pd.DataFrame()

#   #Tien xu ly
#   #Lam bang tay, can cai tien them
#   clean_stock_price = data
#   clean_stock_price = clean_stock_price.drop(index=358) #Truong data CP khong hop le
#   clean_stock_price = clean_stock_price.drop(index=711) #Ma CP khong hop le
#   clean_stock_price = clean_stock_price.reset_index(drop=True)

#   #Xu ly du lieu
#   stock_code_list = []  #Luu ma CP
#   mean_price_list = []  #Luu gia tham chieu trung binh cua CP trong khoang tgian xet
#   choose_by_price_list = [] #1: neu CP co gia trong khoang xet, 0: neu nguoc lai
#   choose_by_volume_list = []  #1: neu CP co khoi luong mua binh thuong, 0: neu nguoc lai

#   for i in range(0, len(clean_stock_price)):
#     stock_code_list.append(clean_stock_price['code'][i])

#     tmp_df = data_convert(clean_stock_price['data'][i], period_long=periodLong)
#     tmp_mean, tmp_check = check_by_price(tmp_df, min_price=minPrice, max_price=maxPrice)
#     mean_price_list.append(tmp_mean)
#     choose_by_price_list.append(tmp_check)

#     tmp_check_2 = check_by_volume(tmp_df)
#     choose_by_volume_list.append(tmp_check_2)
  
#   #Them du lieu hoan chinh vao main_df
#   main_df['Stock_code'] = stock_code_list
#   main_df['Avg_price'] = mean_price_list
#   main_df['Suitable_price'] = choose_by_price_list
#   main_df['Normal_stock'] = choose_by_volume_list

#   #Loc theo khoang gia, mac dinh la (20k, 35k)
#   filter_by_price = main_df[main_df['Suitable_price'] != 0]
#   filter_by_price = filter_by_price.reset_index(drop=True)
  
#   #Loc nhung CP bat thuong
#   final_filter = filter_by_price[filter_by_price['Normal_stock'] != 0]
#   final_filter = final_filter.reset_index(drop=True)

#   #Tra ve danh sach CP duoc chon
#   name_list = []
#   name_list = final_filter['Stock_code'].tolist()

#   #Loc nhung CP co ten Code dai hon 3
#   final_list = []
#   final_list = [x for x in name_list if len(x) == 3]

#   return final_list

#Dung cho file online tren mongo
def filter_stock_mongo(data, minPrice=20.0, maxPrice=35.0, periodLong=30):
  #Tao dataframe luu tat ca cac ma CP va cac gia tri can loc
  main_df = pd.DataFrame()

  #Tien xu ly
  #Lam bang tay, can cai tien them
  clean_stock_price = data
  clean_stock_price = clean_stock_price.drop(index=358) #Truong data CP khong hop le
  clean_stock_price = clean_stock_price.drop(index=711) #Ma CP khong hop le
  clean_stock_price = clean_stock_price.reset_index(drop=True)

  #Xu ly du lieu
  stock_code_list = []  #Luu ma CP
  mean_price_list = []  #Luu gia tham chieu trung binh cua CP trong khoang tgian xet
  choose_by_price_list = [] #1: neu CP co gia trong khoang xet, 0: neu nguoc lai
  choose_by_volume_list = []  #1: neu CP co khoi luong mua binh thuong, 0: neu nguoc lai

  for i in range(0, len(clean_stock_price)):
    stock_code_list.append(clean_stock_price['code'][i])

    tmp_df = data_convert_mongo(clean_stock_price['data'][i], period_long=periodLong)
    tmp_mean, tmp_check = check_by_price(tmp_df, min_price=minPrice, max_price=maxPrice)
    mean_price_list.append(tmp_mean)
    choose_by_price_list.append(tmp_check)

    tmp_check_2 = check_by_volume(tmp_df)
    choose_by_volume_list.append(tmp_check_2)
  
  #Them du lieu hoan chinh vao main_df
  main_df['Stock_code'] = stock_code_list
  main_df['Avg_price'] = mean_price_list
  main_df['Suitable_price'] = choose_by_price_list
  main_df['Normal_stock'] = choose_by_volume_list

  #Loc theo khoang gia, mac dinh la (20k, 35k)
  filter_by_price = main_df[main_df['Suitable_price'] != 0]
  filter_by_price = filter_by_price.reset_index(drop=True)
  
  #Loc nhung CP bat thuong
  final_filter = filter_by_price[filter_by_price['Normal_stock'] != 0]
  final_filter = final_filter.reset_index(drop=True)

  #Tra ve danh sach CP duoc chon
  name_list = []
  name_list = final_filter['Stock_code'].tolist()

  #Loc nhung CP co ten Code dai hon 3
  final_list = []
  final_list = [x for x in name_list if len(x) == 3]

  return final_list

#Luu ket qua

def save_csv_data(list_name, filename):
  dict = {'Code': list_name}
  name_df = pd.DataFrame(dict)
  #Luu file csv
  name_df.to_csv(filename)


#Ket noi den Mongodb

#Ket noi den server: connect_uri, truy cap den database: database_name, lay du lieu tu: collection_name
def connect_mongo(connect_uri, database_name, collection_name):
  client = MongoClient(connect_uri)
  db = client.get_database(database_name)
  mycollection = db[collection_name]
  return client, db, mycollection

def load_data(collection):
  all_records = collection.find()
  list_cursor = list(all_records)
  cursor_df = pd.DataFrame(list_cursor)

  return cursor_df

#Gui du lieu len db
def send_to_mongo(filename, cl_save_name, database):
  csv_df = pd.read_csv(filename)
  send_df = pd.DataFrame()
  send_df['Code'] = csv_df['Code']
  send_dict = send_df.to_dict('record')
  demo_mg = database[cl_save_name]
  demo_mg.insert_many(send_dict)

# FUNCTION_FINAL

#Chay ham nay de thuc hien loc tren mongodb
def filter_from_mongo():
  #Lay du lieu tren mongodb
  CONNECTION_STRING = "mongodb+srv://longpt:longpt@cluster-longpt.ocem8.mongodb.net/test"
  db_name = "stock"
  cl_name = "stock_price_v1"
  client, database, mycollection = connect_mongo(CONNECTION_STRING, db_name, cl_name)
  stock_data = load_data(mycollection)

  #Loc CP
  final_list_mongo = filter_stock_mongo(stock_data)

  #Luu du lieu thanh file csv local
  #filename = '/content/drive/MyDrive/demo_name_stock.csv'
  filename = 'E:/STUDY/UNIVERSITY/Sem_20211/Khoa_hoc_du_lieu/Project/data_stock_name.csv'
  save_csv_data(final_list_mongo, filename)

  #Day du lieu len mongodb
  cl_save_name = "stock_name_v2"
  send_to_mongo(filename, cl_save_name, database)

  #Dong ket noi
  client.close()

#Test
filter_from_mongo()