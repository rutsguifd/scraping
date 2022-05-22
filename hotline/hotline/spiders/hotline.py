import scrapy
from bs4 import BeautifulSoup
from hotline.items import HotlineItem


class HotlineSpider(scrapy.Spider):
    name = 'hotline'
    allowed_domains = ['hotline.ua']
    BASE_URL = 'https://hotline.ua/'
    start_urls = ['https://hotline.ua']

    def start_requests(self):
        yield scrapy.Request(
            url=f'{self.BASE_URL}{self.category_title}/?p=0',
            callback=self.parse
        )

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        last_page = int(soup.find(class_="pagination").find(class_="pages-list cell-sm").find_all(class_="pages")[-1].get('data-page'))
        for i in range(0, last_page + 1):
            yield scrapy.Request(
                url=f'{self.BASE_URL}{self.category_title}/?p={i}',
                callback=self.parse_hotline
            )

    def parse_hotline(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        lines = soup.find(class_="products-list cell-list").find_all(class_="product-item")
        for item in lines:
            try:
                img_href = item.find(class_="item-img").find(class_="item-img-link").find(class_="img-product").get(
                    'src')
                model = item.find(class_="item-info").find(class_="h4").find('a').getText().strip()
                price = item.find(class_="item-price stick-bottom").find(class_="stick-pull cell-xs-6").find(
                    class_="price-md").find(class_="value").getText()
            except AttributeError:
                continue

            yield HotlineItem(
                model=model,
                price=price.replace('\xa0', ' '),
                image_url=f'{self.BASE_URL}{img_href}',
            )