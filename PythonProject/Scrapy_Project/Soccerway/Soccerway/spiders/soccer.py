import scrapy


class SoccerSpider(scrapy.Spider):
    name = 'soccer'
    allowed_domains = ['int.soccerway.com']
    #start_urls = ['https://int.soccerway.com/national/brazil/serie-a/2021/regular-season/r62306/matches']

    def start_requests(self):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
        yield scrapy.Request(url='https://int.soccerway.com/national/brazil/serie-a/2021/regular-season/r62306/matches',headers=headers,callback=self.parse)

    def parse(self, response):
        teama =response.xpath("//td[@class='team team-a ']/a/text()").getall()
        print(teama)
