
import sys
sys.path.append("./demo_api")

import scrapy
import json
from demo_api.items import Sofa_Match
from scrapy.crawler import CrawlerProcess

class sofamatchSpider(scrapy.Spider):
    name = 'sofamatch'
    allowed_domains = ['www.sofascore.com']
    # start_urls = ['http://quotes.toscrape.com/api/quotes?page=1']

    def start_requests(self):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
        yield scrapy.Request(url='https://api.sofascore.com/api/v1/event/9540607/incidents',headers=headers,callback=self.parse)
    

    def parse(self, response):
        raw_data=json.loads(response.body)
        item=Sofa_Match()
        TimeAwayScrore=''
        TimeHomeScrore=''
        for dt in raw_data['incidents']:
            if dt['incidentType']=="period":
                if dt['text']=="FT":
                    item['FTResult']=str(dt['homeScore'])+"-"+str(dt['awayScore'])
                if dt['text']=="HT":
                    item['HTResult']=str(dt['homeScore'])+"-"+str(dt['awayScore'])
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
        
        yield {
                'FTResult':item['FTResult'],
                'HTResult':item['HTResult'],
                'TimeAwayScrore':TimeAwayScrore,
                'TimeHomeScrore':TimeHomeScrore
        }
            
        #yield raw_data
            


process= CrawlerProcess()
process.crawl(sofamatchSpider)
process.start()
        