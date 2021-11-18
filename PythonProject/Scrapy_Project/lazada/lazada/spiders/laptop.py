import sys
sys.path.append("./lazada")

from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from shutil import which
from scrapy_selenium import SeleniumRequest
from scrapy_cloudflare_middleware.middlewares import CloudFlareMiddleware
from scrapy.selector import Selector
import scrapy
from scrapy.crawler import CrawlerProcess
from lazada.items import LazadaItem

class LaptopSpider(scrapy.Spider):
    name = 'laptop'
    allowed_domains = ['www.lazada.vn']
    start_urls = ['https://www.lazada.vn/laptop']

    def start_requests(self):
        chrome_options=Options()
        #chrome_options.add_argument("--headless")
        chrome_path=which("chromedriver")
        driver=webdriver.Chrome(executable_path=chrome_path,options=chrome_options)
        driver.get("https://www.lazada.vn/laptop")
        #rur_tab=driver.find_element_by_xpath('//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a')
        link_elements = WebDriverWait(driver, 100).until(
                        EC.presence_of_all_elements_located((By.XPATH,"//*[@data-qa-locator='product-item']//a"))
                )
        #link_elements=driver.find_element_by_xpath('//*[@data-qa-locator="product-item"]//a')
        for link_el in link_elements:
            href=link_el.get_attribute("href")
            yield scrapy.Request(href,headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
        })
        #self.html=driver.page_source  
    

    def parse(self, response):
        # resp=Selector(text=self.html)
        # for link in resp.xpath("//*[@data-qa-locator='product-item']//a[text()]"):
        #     yield{
        #         'href':link.xpath(".//@href").get()
        #     }
        item=LazadaItem()
        item['name']=response.css('h1 ::text').get()
        item['price']=response.css('.pdp-price_color_orange ::text').get()
        yield item

process= CrawlerProcess()
process.crawl(LaptopSpider)
process.start()
