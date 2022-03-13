from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from myproject.items import Headline


class NewsCrawlSpider(CrawlSpider):
    name = 'news_crawl'
    allowed_domains = ['news.yahoo.co.jp']
    start_urls = ['https://news.yahoo.co.jp/topics/top-picks/']

    # Link をたどるための Rule の List.
    rules = (
        # Topics の page への link をたどり、Response を parse_topics() Method で処理する。
        Rule(LinkExtractor(allow=r'/pickup/\d+$'), callback='parse_topics'),
    )

    def parse_topics(self, response):
        """
        Topics の Page から Title と本文を抜き出す。
        """
        item = Headline()
        item['title'] = response.css('.sc-dLxkki::text').get()
        item['body'] = response.css('.sc-fElddq').xpath('string()').get()
        yield item
