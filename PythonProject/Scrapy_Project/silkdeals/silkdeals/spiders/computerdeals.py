import scrapy
from scrapy_selenium import SeleniumRequest


class ComputerdealsSpider(scrapy.Spider):
    name = 'computerdeals'
    def remove_characters(self, value):
        return value.strip('\xa0')
    # allowed_domains = ['slickdeals.net/computer-deals']
    # start_urls = ['https://slickdeals.net/computer-deals/']
    def start_requests(self):
        yield SeleniumRequest(
            url='https://slickdeals.net/computer-deals/',
            wait_time=3,
            #screenshot=True,
            callback=self.parse

        )

    def parse(self, response):
        products = response.xpath("//ul[@class='dealTiles categoryGridDeals']/li")
        for product in products:
            yield {
                'name': product.xpath(".//a[@class='itemTitle']/text()").get(),
                'link': product.xpath(".//a[@class='itemTitle']/@href").get(),
                'store_name': self.remove_characters(product.xpath("normalize-space(.//span[@class='itemStore']/text())").get()),
                'price': product.xpath("normalize-space(.//div[@class='itemPrice  wide ']/text())").get()
            }
        next_page = response.xpath("//a[@data-role='next-page']/@href").get()
        if next_page:
            absolute_url = f"https://slickdeals.net{next_page}"
            yield SeleniumRequest(
                url=absolute_url,
                wait_time=3,
                callback=self.parse
            )
