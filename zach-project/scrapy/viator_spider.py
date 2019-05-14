import scrapy
from scrapy import Selector
from pymongo import MongoClient
class MyViatorSpider(scrapy.Spider):
    name = 'viator'
    start_urls = ['https://www.viator.com/Paris/d479-ttd']

    def __init__(self):
        connection = MongoClient("localhost",27017)
        db = connection["traveldata"]
        self.collection = db["viatordata"]
    def parse(self, response):
        print(response)

        titles = response.xpath("//div[@class='product-card-main-content']").extract()

        print(titles)
        for t in titles:
            sel = Selector(text = t)
            dict_info = {
                'img':sel.xpath('//img/@data-src').extract()[0],
                'title':sel.xpath('//h2/a/text()').extract()[0],
                'price':sel.xpath('//div[@class="font-weight-bold h3 mb-0"]/text()').extract_first()
            }
            #yield dict_info
            self.collection.insert(dict_info)
       

from scrapy.crawler import CrawlerProcess

c = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0',
    'FEED_FORMAT': 'json',
    'FEED_URI': 'output.json',
})
c.crawl(BrickSetSpider)
c.start()