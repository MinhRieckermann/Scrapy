import sys
sys.path.append("./coinmarketcap")


from cssselect import xpath
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
import urllib.parse
from coinmarketcap.items import Sofa_Match
import json


class FootballScrapeSpider(scrapy.Spider):
    name = 'football_scrape'
    allowed_domains = ['www.sofascore.com']
    start_urls = ['https://www.sofascore.com/tournament/football/brazil/brasileiro-serie-a/325']
    item=Sofa_Match()
    headers={
        'accept':'*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7,de-DE;q=0.6,de;q=0.5',
        'referer': 'https://www.sofascore.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
    }

    
    def start_requests(self):
        api_event_url='https://www.sofascore.com/api/v1/event/{0}/h2h/events' #https://web.archive.org/web/20211023110834/
        chrome_options=Options()
        #chrome_options.add_argument("--headless")
        chrome_path=which("chromedriver")
        driver=webdriver.Chrome(executable_path=chrome_path,options=chrome_options)


        driver.get('https://www.sofascore.com/tournament/football/brazil/brasileiro-serie-a/325')#https://web.archive.org/web/20211023110834/
        results = []
        tab_selector='//div[@class="u-mV12"]/div/div[contains(@class,"Tabs__Header")]/a[text()="By Round"]'

        by_Round=WebDriverWait(driver, 4000).until(
                                EC.presence_of_element_located((By.XPATH,tab_selector))
                                )
        by_Round.click()

        by_Round=WebDriverWait(driver, 4000).until(
                                EC.presence_of_element_located((By.XPATH,tab_selector))
                                )

        data_url=WebDriverWait(driver, 1000).until(
                       EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a' ))
                       )
        hometeam=WebDriverWait(driver, 100).until(
                                            EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a/div/div[contains(@class,"EventCellstyles__EventCell")]/div[3]/div[1]'))
                                            )
        awayteam=WebDriverWait(driver, 100).until(
                                            EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a/div/div[contains(@class,"EventCellstyles__EventCell")]/div[3]/div[2]'))
                                            )
        time_match=WebDriverWait(driver, 100).until(
                                            EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a/div/div/div[contains(@class,"EventCellstyles__Status")]/div[1]'))
                                            )
        driver.implicitly_wait(60)

        body=driver.page_source

        resp=Selector(text=body)

        country=resp.xpath("//span[contains(@class,'styles__CategoryName')]/text()[2]").get()
        tournament=resp.xpath("//h2/text()").get()
        year=resp.xpath("//button[contains(@class,'styles__Selector')]/span/text()").get()
        round_match=resp.xpath("//div[contains(@class,'list-wrapper')]/div[contains(@class,'styles__EventListHeader')]/div[2]/div/div/button/span/text()").get()
        for i in range(len(data_url)):
            data_url=WebDriverWait(driver, 1000).until(
                            EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a' ))
                            )
            hometeam=WebDriverWait(driver, 100).until(
                                            EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a/div/div[contains(@class,"EventCellstyles__EventCell")]/div[3]/div[1]'))
                                            )
            awayteam=WebDriverWait(driver, 100).until(
                                            EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a/div/div[contains(@class,"EventCellstyles__EventCell")]/div[3]/div[2]'))
                                            )
            time_match=WebDriverWait(driver, 100).until(
                                            EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a/div/div/div[contains(@class,"EventCellstyles__Status")]/div[1]'))
                                            )
            
            link_code=urllib.parse.urlparse(data_url[i].get_attribute('href'))
            path=link_code[2].rpartition('/')
            detail={
            'country':country,
            'tournament':tournament,
            'year':year,
            'hometeam':hometeam[i].text,
            'awayteam':awayteam[i].text,
            'time_match':time_match[i].text,
            'round_match':round_match,
            'detail_url':data_url[i].get_attribute('href'),
            'code':path[2]



                }
            results.append(detail)
        driver.implicitly_wait(400)
        next_url=WebDriverWait(driver, 400).until(
                       EC.presence_of_element_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListHeader")]/div[1]/div' ))
                       )
        



        data=WebDriverWait(driver, 100).until(
                       EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a' ))
                       )
        while next_url:
            try:
                next_url.click()

                data=WebDriverWait(driver, 100).until(
                                EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a' ))
                                )
                hometeam=WebDriverWait(driver, 100).until(
                                            EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a/div/div[contains(@class,"EventCellstyles__EventCell")]/div[3]/div[1]'))
                                            )
                awayteam=WebDriverWait(driver, 100).until(
                                            EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a/div/div[contains(@class,"EventCellstyles__EventCell")]/div[3]/div[2]'))
                                            )
                time_match=WebDriverWait(driver, 100).until(
                                            EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a/div/div/div[contains(@class,"EventCellstyles__Status")]/div[1]'))
                                            )
                round_match=WebDriverWait(driver, 10).until(
                                            EC.presence_of_element_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListHeader")]/div[2]/div/div/button/span'))
                                            )
                
                for i in range(len(data)):
                    data=WebDriverWait(driver, 1000).until(
                                    EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a' ))
                                    )
                    link_code=urllib.parse.urlparse(data[i].get_attribute('href'))
                    path=link_code[2].rpartition('/')
                    detail={
                            'country':country,
                            'tournament':tournament,
                            'year':year,
                            'hometeam':hometeam[i].text,
                            #driver.find_element_by_xpath('//div/div[contains(@class,"EventCellstyles__EventCell")]/div[3]/div[1]').text,
                            'awayteam':awayteam[i].text,
                            #driver.find_element_by_xpath('//div/div[contains(@class,"EventCellstyles__EventCell")]/div[3]/div[2]').text,
                            'time_match':time_match[i].text,
                            #driver.find_element_by_xpath('//div/div/div[contains(@class,"EventCellstyles__Status")]/div[1]').text,
                            'round_match':round_match.text,
                            #driver.find_element_by_xpath('//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListHeader")]/div[2]/div/div/button/span').text,
                            'detail_url':data[i].get_attribute('href'),
                            'code':path[2]


                            }
                    
                    results.append(detail)
                    
            except:
                break
        driver.close()

        for event in results:
            event["api_event_url"]=api_event_url.format(event.get("code"))
        
        for event in results:
            self.item['season']=event.get("year")
            self.item['roundInfo']=event.get("round_match")
            self.item['time_match']=event.get("time_match")
            self.item['country']=event.get("country")
            self.item['tournament']=event.get("tournament")
        #self.item['roundInfo']=roundInfo
            self.item['Hometeam']=event.get("Hometeam")
            self.item['Awayteam']=event.get("Awayteam")
            yield scrapy.Request(url=event.get("api_event_url"),callback=self.parse,headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
            }
            )
        


    def parse(self, response):
        raw_data=json.loads(response.body)
        item=Sofa_Match()
        tournament=''
        country=''
        roundInfo=''
        Hometeam=''
        Awayteam=''
        match_id=''
        tournament=raw_data['events'][0]['tournament']['name']
        country=raw_data['events'][0]['tournament']['category']['name']
        roundInfo=raw_data['events'][0]['roundInfo']['round']
        Hometeam=raw_data['events'][0]['homeTeam']['name']
        Awayteam=raw_data['events'][0]['awayTeam']['name']
        match_id=raw_data['events'][0]['id']

        api_detail_url='https://www.sofascore.com/api/v1/event/{0}/incidents'#https://web.archive.org/web/20211023110834/
        detail_url=api_detail_url.format(match_id)
        # item['HTResult']=
        # item['HomeScores']=
        # item['AwayScores']=
        # item['TimeAwayScrore']=
        # item['TimeHomeScrore']=
        # item['DetailScore']=
        

        yield scrapy.Request(url=detail_url,callback=self.parse_api,headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
            }
            )
    def parse_api(self,response):

        raw_data=json.loads(response.body)
        item=Sofa_Match()
        TimeAwayScrore=''
        TimeHomeScrore=''
        FTResult=''
        HTResult=''
        for dt in raw_data['incidents']:
            if dt['incidentType']=="period":
                if dt['text']=="FT":
                    FTResult=str(dt['homeScore'])+"-"+str(dt['awayScore'])
                if dt['text']=="HT":
                    HTResult=str(dt['homeScore'])+"-"+str(dt['awayScore'])
            if dt['incidentType']=="goal":
                if dt['isHome']==False:
                    TimeAwayScrore=TimeAwayScrore+str(dt['time'])+";"
                if dt['isHome']==True:
                    TimeHomeScrore=TimeHomeScrore+str(dt['time'])+";"
                    # item['HTResult']=
                    # item['HomeScores']=
                    # item['AwayScores']=
                    # item['TimeAwayScrore']=
                    # item['TimeHomeScrore']=
                    # item['DetailScore']=
                    # item['Hometeam']=
                    # item['Awayteam']=
                    # item['country']=
                    # item['tournament']=
                    # item['season']=
        
        
        self.item['FTResult']=FTResult
        self.item['HTResult']=HTResult
        self.item['TimeAwayScrore']=TimeAwayScrore
        self.item['TimeHomeScrore']=TimeHomeScrore
        self.item['DetailScore']=TimeHomeScrore+"-"+TimeAwayScrore
        
        #yield self.item

        yield {
                'country':self.item['country'],
                'tournament':self.item['tournament'],
                'season':self.item['season'],
                'roundInfo':self.item['roundInfo'],
                'time_match':self.item['time_match'],
                'Hometeam':self.item['Hometeam'],
                'Awayteam':self.item['Awayteam'],
                'FTResult':self.item['FTResult'],
                'HTResult':self.item['HTResult'],
                'TimeAwayScrore':self.item['TimeAwayScrore'],
                'TimeHomeScrore':self.item['TimeHomeScrore'],
                'DetailScore':self.item['DetailScore']

            }


process= CrawlerProcess()
process.crawl(FootballScrapeSpider)
process.start()
