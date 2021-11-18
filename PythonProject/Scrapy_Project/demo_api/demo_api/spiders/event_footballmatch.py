import sys
sys.path.append("./demo_api")

import scrapy
import json
from demo_api.items import Sofa_Match
from scrapy.crawler import CrawlerProcess
import urllib
from scrapy import Request


class EventFootballmatchSpider(scrapy.Spider):
    name = 'event_footballmatch'
    allowed_domains = ['www.sofascore.com']
    #start_urls = ['http://www.sofascore.com/']
    item=Sofa_Match()

    def start_requests(self):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
        yield scrapy.Request(url='https://www.sofascore.com/api/v1/event/kPsrP/h2h/events',headers=headers,callback=self.parse)
    

    def parse(self, response):

        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}

        raw_data=json.loads(response.body)
        
        
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

        self.item['country']=country
        self.item['tournament']=tournament
        self.item['roundInfo']=roundInfo
        self.item['Hometeam']=Hometeam
        self.item['Awayteam']=Awayteam
        

        api_detail_url='https://www.sofascore.com/api/v1/event/{0}/incidents'
        detail_url=api_detail_url.format(match_id)
        yield scrapy.Request(url='https://www.sofascore.com/api/v1/event/9540523/incidents',headers=headers,callback=self.parse_api)
        # for dt in raw_data['events']:
        #     if dt['incidentType']=="period":
        #         if dt['text']=="FT":
        #             item['FTResult']=str(dt['homeScore'])+"-"+str(dt['awayScore'])
        #         if dt['text']=="HT":
        #             item['HTResult']=str(dt['homeScore'])+"-"+str(dt['awayScore'])
        #     if dt['incidentType']=="goal":
        #         if dt['isHome']==False:
        #             TimeAwayScrore=TimeAwayScrore+str(dt['time'])+";"
        #         if dt['isHome']==True:
        #             TimeHomeScrore=TimeHomeScrore+str(dt['time'])+";"
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
        
    def parse_api(self,response):

        raw_data=json.loads(response.body)
        
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
        
        yield self.item
        


process= CrawlerProcess()
process.crawl(EventFootballmatchSpider)
process.start()