import scrapy


class FacultItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()


class DepartmentItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()


class StaffItem(scrapy.Item):
    name = scrapy.Field()