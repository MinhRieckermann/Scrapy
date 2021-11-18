import scrapy
from scrapy import selector
from scrapy.item import Item
from scrapy.loader import ItemLoader
from books_to_scrape.items import BooksToScrapeItem
from scrapy.selector import Selector

class ImagespiderSpider(scrapy.Spider):
    name = 'downloader'
    #allowed_domains = ['openlibrary.org']
    start_urls = ['https://books.toscrape.com']

    def parse(self, response):
        for article in response.xpath(".//article[@class='product_pod']"):
            loader=ItemLoader(item=BooksToScrapeItem(),selector=article)
            relative_url=article.xpath(".//div[@class='image_container']/a/img/@src").extract_first()
            absolute_url=response.urljoin(relative_url)
            loader.add_value('image_urls',absolute_url)
            loader.add_xpath('book_name',".//h3/a/@title")
            yield loader.load_item()
