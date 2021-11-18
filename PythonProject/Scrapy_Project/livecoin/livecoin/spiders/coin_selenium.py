

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

class CoinSeleniumSpider(scrapy.Spider):
    name = 'coin_selenium'
    allowed_domains = ['web.archive.org']
    start_urls = ['http://web.archive.org/web/20210920215806/https://www.sofascore.com/tournament/football/brazil/brasileiro-serie-b/390']
    
    custom_settings = {
        'FEEDS' : {
            'data.csv':{
                'format':'csv'
            }
        }
    }
    def __init__(self):
        chrome_options=Options()
        #chrome_options.add_argument("--headless")
        chrome_path=which("chromedriver")
        driver=webdriver.Chrome(executable_path=chrome_path,options=chrome_options)
        driver.get("http://web.archive.org/web/20210920215806/https://www.sofascore.com/tournament/football/brazil/brasileiro-serie-b/390")
        #rur_tab=driver.find_element_by_xpath('//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a')
        # link_elements = WebDriverWait(driver, 100).until(
        #                 EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a'))
        #         )
        self.html=driver.page_source      
        #driver.close() 

    def parse(self, response):
        resp=Selector(text=self.html)
        for link in resp.xpath("//div[contains(@class,'list-wrapper')]/div[contains(@class,'styles__EventListContent')]/a"):
            yield{
                'hometeam':link.xpath(".//div/div[contains(@class,'EventCellstyles__EventCell')]/div[3]/div[1]/text()").get(),
                'awayteam':link.xpath(".//div/div[contains(@class,'EventCellstyles__EventCell')]/div[3]/div[2]/text()").get(),
                'time_match':link.xpath(".//div/div/div[contains(@class,'EventCellstyles__Status')]/div[1]/text()").get(),
                'detail_url':link.xpath(".//@href").get()

            }
        
process= CrawlerProcess()
process.crawl(CoinSeleniumSpider)
process.start()
