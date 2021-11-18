import scrapy
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from shutil import which
from Wikipedia.items import LaptopItem

class LaptopSpider(scrapy.Spider):
    name = 'Laptop'
    allowed_domains = ['www.lazada.vn']
    start_urls = ['https://www.lazada.vn/laptop']


    def start_requests(self):
        chrome_options=Options()
        chrome_options.add_argument("--headless")
        chrome_path=which("chromedriver")
        driver=webdriver.Chrome(executable_path=chrome_path,options=chrome_options)
        driver.get('https://www.lazada.vn/laptop')
        link_elements=driver.find_element_by_xpath('//*[@data-qa-locator="product-item"]//a[text()]')
        #link=[]
        for link_el in link_elements:
            href=link_el.get_attribute("href")
            yield scrapy.Request(href)
            #print(href)
            #link.append(href)
        driver.quit()

    def parse(self, response):
        item=LaptopItem()
        item['name']=response.css('h1 ::text').get()
        item['price']=response.css('.pdp-price_color_orange ::text').get()
        yield item
