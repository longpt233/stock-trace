from urllib import parse
from scrapy import Spider, Request
import scrapy
from scrapy.selector import Selector
from crawler.items import CrawlerItem

class CrawlerSpider(Spider):
    name = "crawler"
    # allowed_domains = ["thegioididong.com"]
    start_urls = [
        # "https://evnhanoi.vn/api/index.html?url=/api/specification.json#/App",
        # "https://www.thegioididong.com/dtdd/samsung-galaxy-a50",
        # 'https://sohoa.vnexpress.net/tin-tuc/doi-song-so/tap-chi-co-chu-ky-steve-jobs-duoc-ban-gia-50-000-usd-3662652.html'
        'https://vnexpress.net/category/day?cateid=1003159&fromdate=1633046400&todate=1633305600&allcate=1003159'
    ]
    

    # def start_requests(self):
    #     urls = [
    #         'https://vnexpress.net/category/day?cateid=1003159&fromdate=1633046400&todate=1633305600&allcate=1003159',
    #     ]
    #     for url in urls:
    #         yield Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # page = 'test'
        # filename = f'evn-{page}.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved file {filename}')
        
        questions = Selector(response).xpath('//div[@class="width_common list-news-subfolder has-border-right"]/article')
        # print(questions)
        for question in questions:
            item = CrawlerItem()
            item['Title'] = question.xpath('h3[@class="title-news"]/a/text()').extract_first()
            item['Description'] = question.xpath('p[@class="description"]/a/text()').extract_first()
            item['MetaData'] = 'not yet'
            # item['MetaData'] = question.xpath('p[@class="meta-news"]/a/text()')
            print('item ', item)
            
            yield item
        
        # artilce = {}
        # # artilce['title'] = response.xpath('//h1/text()').get()
        # artilce['title'] = response.css('h3.titles-news a::text').get(default='')
        # artilce['description'] = response.xpath('//p[@class = "description"]/text()').extract()
        
        # request next page
        # link = response.css('a::attr(herf)').get()
        # if link is not None:
            # way1
            # next_page = response.urljoin(next_page)
            # yield scrapy.Request(next_page, callback=self.parse
            
            # way 2
        #     yield response.follow(link, callback=self.parse)
        # for key, text in artilce.items():
        #     print ("{key}: {text}".format(key = key.upper(), text = text))


# Run scrap 
# file json:
# scrapy crawl crawler -o comments.json
# hoặc file csv:
# scrapy crawl crawler -o comments.csv
