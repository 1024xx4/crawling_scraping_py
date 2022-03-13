import scrapy


class TabelogSpider(scrapy.Spider):
    name = 'tabelog'
    allowed_domains = ['tabelog.com']
    start_urls = ['http://tabelog.com/']

    def parse(self, response):
        pass
