# from crawl import DataLoaderCAFE
#
# symboi ="AAS"
#
# loader = DataLoaderCAFE(symbol=symboi, start="2021-09-10", end="2021-09-10")
# try:
#     data = loader.download()
#     data = data[::-1]
#     print(data.head(1))
#     data.to_csv("../../data/csv-30/"+symboi+".csv",index=False,header=True, mode= 'a')
# except:
#     print("err ")

# line = "2021-09-12 1"
# last_time_crawl= str(line).split(" ")[0]
# print(last_time_crawl)

# import datetime

# last_time_crawl = datetime.datetime.strptime(last_time_crawl+  ' 1:33PM', '%Y-%m-%d %I:%M%p')

# today = str(last_time_crawl + datetime.timedelta(days=1)).split(" ")[0]


from vndirect import DataLoaderVnDirect
import datetime


yesterday = str(datetime.datetime.now() - datetime.timedelta(days=1)).split(" ")[0]

dir_csv = "all"

next_day_of_last_time = ''
with open('../../data/vndirect/'+dir_csv+'/1-log-crawl.txt', 'rt') as f:
    for line in f:
        pass
    last_time_crawl= str(line).split(" ")[0]
    last_time_crawl = datetime.datetime.strptime(last_time_crawl+  ' 1:33PM', '%Y-%m-%d %I:%M%p')
    next_day_of_last_time = str(last_time_crawl + datetime.timedelta(days=1)).split(" ")[0]
    print(next_day_of_last_time)

loader = DataLoaderVnDirect(symbol="AAM", start=next_day_of_last_time, end="2021-09-30")
# try:
data = loader.download()[::-1] # to revert 
print(data)
# except:
#     print("err ")

