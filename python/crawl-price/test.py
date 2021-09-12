from crawl import DataLoaderCAFE

# loader = DataLoaderCAFE(symbol= "ACB", start="2021-02-01", end="2021-03-01")
# try:
#     data = loader.download()
#     data = data[::-1]
#     data.to_csv("../../data/csv-30/"+"ACB"+".csv",index=False,header=False, mode= 'a')
# except:
#     print("err ")

line = "2021-09-12 1"
last_time_crawl= str(line).split(" ")[0]
print(last_time_crawl)

import datetime

last_time_crawl = datetime.datetime.strptime(last_time_crawl+  ' 1:33PM', '%Y-%m-%d %I:%M%p')

today = str(last_time_crawl + datetime.timedelta(days=1)).split(" ")[0]

