import scrapy
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.options import Options
from shutil import which
from scrapy_selenium import SeleniumRequest
from scrapy_cloudflare_middleware.middlewares import CloudFlareMiddleware
from scrapy.selector import Selector


class SofascoresSpider(scrapy.Spider):
    name = 'sofascores'
    # allowed_domains = ['www.sofascore.com']
    # start_urls = ['http://web.archive.org/web/20210920215806/https://www.sofascore.com/tournament/football/brazil/brasileiro-serie-b/390']

    def start_requests(self):
        yield SeleniumRequest(
            url='http://web.archive.org/web/20210920215806/https://www.sofascore.com/tournament/football/brazil/brasileiro-serie-b/390',
            wait_time=3,
            screenshot=True,
            callback=self.parse

        )
    # def __init__(self):
    #     self.path_to_html = html_path + 'index.html'
    #     self.path_to_header = 'D:/Python Learning/Scrapy/PythonProject/Scrapy_Project' + 'index.html'
    #     self.html_file = open(self.path_to_html, 'w')
    # def __init__(self):
    #     chrome_options=Options()
    #     chrome_options.add_argument("--headless")
    #     chrome_path=which("chromedriver")
    #     driver=webdriver.Chrome(executable_path=chrome_path,options=chrome_options)
    #     driver.get("https://www.sofascore.com/tournament/football/italy/serie-a/23")
    #     rur_tab=driver.find_element_by_xpath("//div[contains(@class,'list-wrapper')]/div[contains(@class,'styles__EventListContent')]/a")

    #     self.html=driver.page_source      
    #     driver.close()  

    # def start_requests(self):
    #     yield scrapy.Request(url='https://www.sofascore.com/tournament/football/italy/serie-a/23',callback=self.parse,headers={
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
    #     })
    def parse(self, response):
        #yield response.xpath("//div[contains(@class,'list-wrapper')]/div[contains(@class,'styles__EventListContent')]/a/@href").getall()
        driver=response.meta['driver']
        html=driver.page_source
        # response_obj=Selector(text=html)
        
        #print(html)
        #filename = response.url.split("/")[-1] + '.html'
        filename=Selector(text=html)
        with open(filename, 'wb') as f:
            f.write(response.body)
           

