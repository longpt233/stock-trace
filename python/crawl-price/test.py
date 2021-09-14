from crawl import DataLoaderCAFE

symboi ="AAS"

loader = DataLoaderCAFE(symbol=symboi, start="2021-09-10", end="2021-09-10")
try:
    data = loader.download()
    data = data[::-1]
    print(data.head(1))
    data.to_csv("../../data/csv-30/"+symboi+".csv",index=False,header=True, mode= 'a')
except:
    print("err ")

# line = "2021-09-12 1"
# last_time_crawl= str(line).split(" ")[0]
# print(last_time_crawl)

# import datetime

# last_time_crawl = datetime.datetime.strptime(last_time_crawl+  ' 1:33PM', '%Y-%m-%d %I:%M%p')

# today = str(last_time_crawl + datetime.timedelta(days=1)).split(" ")[0]


loader = DataLoaderVnDirect(symbol="AAM", start="2010-10-10", end="2021-09-15")
try:
    data = loader.download()[::-1] # to revert 
    data.to_csv("../../data/vndirect/csv-10-30/"+"AAM"+".csv",index=True,header=False)
except:
    print("err ")

