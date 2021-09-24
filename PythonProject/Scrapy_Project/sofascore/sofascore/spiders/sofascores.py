import scrapy


class SofascoresSpider(scrapy.Spider):
    name = 'sofascores'
    allowed_domains = ['www.sofascore.com']
    start_urls = ['https://www.sofascore.com/']

    def parse(self, response):
        pass
