from typing import KeysView
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector


class ExampleSpider(scrapy.Spider):
    name = 'example'
   
    def start_requests(self):
        yield SeleniumRequest(
            #url='https://duckduckgo.com',
            url='http://web.archive.org/web/20210920215806/https://www.sofascore.com/tournament/football/brazil/brasileiro-serie-b/390',
            wait_time=3,
            screenshot=True,
            callback=self.parse

        )
    def parse(self, response):
        # img=response.meta['screenshot']
        # with open('screenshot.png','wb') as f:
        #     f.write(img)
        driver=response.meta['driver']
        #search_input=driver.find_element_by_xpath("//input[@id='search_form_input_homepage']")
        #search_input.send_keys('Hello world')
        #driver.save_screenshot('after_filling_input.png')
        #search_input.send_keys(Keys.ENTER)

        html=driver.page_source
        response_obj=Selector(text=html)
        # links=response_obj.xpath("//div[@class='result__extras__url']/a")
        # for link in links:
        #     yield{
        #         'URL':link.xpath(".//@href").get()
        #     }
       
        filename=Selector(text=html)
        with open(filename, 'wb') as f:
            f.write(response.body)


