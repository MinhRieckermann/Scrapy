import scrapy
import json


class sofamatchSpider(scrapy.Spider):
    name = 'sofamatch'
    allowed_domains = ['www.sofascore.com']
    # start_urls = ['http://quotes.toscrape.com/api/quotes?page=1']

    def start_requests(self):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
        yield scrapy.Request(url='https://api.sofascore.com/api/v1/unique-tournament/1258/season/35977/team-events/total',headers=headers,callback=self.parse)


    def parse(self, response):
        reps=json.loads(response.body)
        print(reps)