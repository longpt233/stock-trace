# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from sys import getsizeof
# import time
# import csv
# import random


# PROXY = "58.26.138.171:80"


# proxyList = [
#     '171.232.74.123:45006',
#     '116.105.20.208:4001',
#     '47.243.233.113:59394'
# ]


# class Article:
#     def __init__(self, title, meta, desc, link):
#         self.title = title
#         self.meta = meta
#         self.desc = desc
#         self.link = link
        
# # 'https://tinnhanhchungkhoan.vn/chung-khoan/'
# url = 'https://thoibaotaichinhvietnam.vn/chung-khoan'

# # options = Options()
# # # options.add_argument('--headless')
# # options.add_argument('--proxy-server={}'.format(proxyList[0]))
# # # options.add_argument("--proxy-server=socks5://{}".format(random.choice(proxyList)))
# # browser = webdriver.Chrome(executable_path='E:\chromedriver.exe', options=options)
# # # browser = webdriver.Chrome(executable_path='E:\chromedriver.exe',desired_capabilities=capabilities , options=options)

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# # options.add_argument('--proxy-server=%s' % PROXY)
# browser = webdriver.Chrome(executable_path='E:\chromedriver.exe',chrome_options=options)

# # WebDriverWait wait = new WebDriverWait(browser, 30);

# data = []
# # url = 'https://thoibaotaichinhvietnam.vn/chung-khoan&s_cond=&BRSR=0'
# # browser.get(url)
# # soup = BeautifulSoup(browser.page_source, 'html.parser')
# # list_article = soup.select('.article-bdt-20 div article')

# # for article in list_article:
# #     info = article.select_one('div')
    
# #     link = info.select_one('h3 a')['href']
# #     title = info.select_one('h3 a')['title']
# #     meta = info.select_one('div.article-meta span span.format_date').text
# #     desc = info.select_one('div.article-desc').getText()
# #     data.append(Article(title, meta, desc, link))

# # print(len(data))
# # for article in data:
# #     print([article.title, article.meta, article.link, article.desc])
# # browser.quit()




# def get_data(data, page, j):
#     soup = BeautifulSoup(browser.page_source, 'html.parser')
#     list_article = soup.select('.article-bdt-20 div article')
#     for article in list_article:
#         info = article.select_one('div')
#         link = info.select_one('h3 a')['href']
#         title = info.select_one('h3 a')['title']
#         meta = info.select_one('div.article-meta span span.format_date').text
#         desc = info.select_one('div.article-desc').getText()
#         data.append(Article(title, meta, desc, link))
        
#     return True


# start = time.time()
# page = 'https://thoibaotaichinhvietnam.vn/chung-khoan&s_cond=&BRSR={}'
# for i in range(660):
#     url = page.format(i*15)
#     print(url)
#     browser = webdriver.Chrome(executable_path='E:\chromedriver.exe', options=options)
#     browser.get(url)
#     soup = BeautifulSoup(browser.page_source, 'html.parser')
#     list_article = soup.select('.article-bdt-20 div article')

#     for article in list_article:
#         info = article.select_one('div')
#         link = info.select_one('h3 a')['href']
#         title = info.select_one('h3 a')['title']
#         meta = info.select_one('div.article-meta span span.format_date').text
#         desc = info.select_one('div.article-desc').getText()
#         data.append(Article(title, meta, desc, link))
#     browser.quit()
#     time.sleep(5)
        
# print(len(data))
# print(getsizeof(data))
# print(time.time() - start)



# # data = [Article('trường', '2', '3', '4')]
# def write_file():
#     filepath = 'E:/data.csv'
#     file = open(filepath, 'w', encoding='utf-8')
#     file_CSV = csv.writer(file)
#     for article in data:
#         file_CSV.writerow([article.title, article.meta, article.link, article.desc])
#     file.close()
    
# write_file()

# browser.quit()
# print('done')

# 'https://tinnhanhchungkhoan.vn/api/contents/get/by-next-page?list_id=1&list_type=12&page_index=2&page_size=30&page_type=LIST_ZONE'
# # https://tinnhanhchungkhoan.vn/api/contents/get/by-next-page?list_id=1&list_type=12&page_index=4&page_size=30&page_type=LIST_ZONE  

# def crawl_data_evn_by_day(url):
#     browser.get(url)
#     data = [[] for i in range(3)]
#     queue = []

#     get_data_table(data, queue, 2)

#     indexes = [i for i in range(2, 6)]
#     i = 0
#     while queue:
#         index_a = indexes[i%4]
#         a = browser.find_element_by_css_selector(f'.pagination-ys > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child({index_a}) > a:nth-child(1)')
#         print('a text ==', a.text)
#         browser.execute_script(a.get_attribute('href'))
#         time.sleep(1)
#         queue.pop()
#         if i == 3:
#             indexes = [j+1 for j in indexes]

#         index_next = indexes[(i+1)%4]
#         get_data_table(data, queue, index_next)
#         i += 1
    
#     return data

import csv 
file = open('Data_Science/stock-trace/crawl-module-v2/crawl_article/article.csv', 'r', encoding='utf-8')
filecsv = csv.reader(file)
for i, row in enumerate(filecsv):
    
    # if i < 10:
    #     break
    print(i, row)
file.close()


