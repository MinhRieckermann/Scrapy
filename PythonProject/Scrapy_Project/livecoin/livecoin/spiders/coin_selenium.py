import scrapy
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.options import Options
from shutil import which
from scrapy_selenium import SeleniumRequest
from scrapy_cloudflare_middleware.middlewares import CloudFlareMiddleware

class CoinSeleniumSpider(scrapy.Spider):
    name = 'coin_selenium'
    allowed_domains = ['web.archive.org']
    start_urls = ['http://web.archive.org/web/20210920215806/https://www.sofascore.com/tournament/football/brazil/brasileiro-serie-b/390']

    def __init__(self):
        chrome_options=Options()
        chrome_options.add_argument("--headless")
        chrome_path=which("chromedriver")
        driver=webdriver.Chrome(executable_path=chrome_path,options=chrome_options)
        driver.get("http://web.archive.org/web/20210920215806/https://www.sofascore.com/tournament/football/brazil/brasileiro-serie-b/390")
        rur_tab=driver.find_element_by_xpath("//div[contains(@class,'list-wrapper')]/div[contains(@class,'styles__EventListContent')]/a")

        self.html=driver.page_source      
        driver.close() 

    def parse(self, response):
        print(self.html)
