import sys
sys.path.append("./sofascore")
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from sofascore.spiders.footballscrape import FootballscrapeSpider


process= CrawlerProcess(settings=get_project_settings())
process.crawl(FootballscrapeSpider)
process.start()