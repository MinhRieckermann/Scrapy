# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class CoinmarketcapItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class Sofa_Match(Item):
    country=Field()
    tournament=Field()
    season=Field()
    roundInfo=Field()
    time_match=Field()
    Hometeam=Field()
    Awayteam=Field()
    FTResult=Field()
    HTResult=Field()

    HomeScores=Field()
    AwayScores=Field()
    TimeAwayScrore=Field()
    TimeHomeScrore=Field()
    DetailScore=Field()
    
    

    Recard=Field()