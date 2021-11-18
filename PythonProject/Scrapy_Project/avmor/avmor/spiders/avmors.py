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

class AvmorsSpider(scrapy.Spider):
    name = 'avmors'
    allowed_domains = ['www.avmor.com']
    start_urls = ['https://www.avmor.com']


    def start_requests(self):
        chrome_options=Options()
        #chrome_options.add_argument("--headless")
        chrome_path=which("chromedriver")
        driver=webdriver.Chrome(executable_path=chrome_path,options=chrome_options)
        driver.get("https://www.avmor.com/products")
        #rur_tab=driver.find_element_by_xpath('//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a')
        link_elements = WebDriverWait(driver, 100).until(
                        EC.presence_of_all_elements_located((By.XPATH,"//div[@class='title-wrapper']//a"))
                )
        #link_elements=driver.find_element_by_xpath('//*[@data-qa-locator="product-item"]//a')
        for link_el in link_elements:
            href=link_el.get_attribute("href")
            yield scrapy.Request(href,headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
        })
    def parse(self, response):
        productname = response.xpath("//div[@class='product-title-container']/h1//text()")
        desc =response.xpath("//div[@class='tabbed-content']/div[@class='tab-panels']/div[@id='tab_description']/text()")
        images=[]
        for img in response.xpath("//div[contains(@class,'woocommerce-product-gallery__image')]/a"):
            images.append(img.xpath(".//@href").get())
        yield{
            'name':productname.get(),
            'desc':desc.get(),
            'images':[images]
        }
