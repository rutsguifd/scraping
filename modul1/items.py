import scrapy


class BathItem(scrapy.Item):
    model = scrapy.Field()
    model_url = scrapy.Field()
    shops = scrapy.Field()
    start_price = scrapy.Field()
    end_price = scrapy.Field()
    img_url = scrapy.Field()
    image_urls = scrapy.Field()