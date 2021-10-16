import scrapy
import json

class QoutesSpider(scrapy.Spider):
    name = 'qoutes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/api/quotes?page=1']

    def parse(self, response):
        reps=json.loads(response.body)
        quotes=reps.get('quotes')
        for quote in quotes:
            yield{
                'author': quote.get('author').get('name'),
                'tags':quote.get('tags'),
                'quote_text':quote.get('text'),
            }
        has_next=reps.get('has_next')
        if has_next:
            next_page_number=reps.get('page')+1
            yield scrapy.Request(
                url=f'http://quotes.toscrape.com/api/quotes?page={next_page_number}',
                callback=self.parse
            )