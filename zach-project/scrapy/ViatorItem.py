import scrapy

class ViatorItem(scrapy.Item):

    title = scrapy.Field()
    img = scrapy.Field()
    price = scrapy.Field()