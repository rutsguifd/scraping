
import scrapy


class ComputerItem(scrapy.Item):
    model = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()