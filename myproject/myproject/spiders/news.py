import scrapy

from myproject.items import Headline  # Item の Headline class を import.


class NewsSpider(scrapy.Spider):
    name = 'news'  # Spider の名前
    allowed_domains = ['news.yahoo.co.jp']  # Crawl 対象とする Domain の List
    start_urls = ['https://news.yahoo.co.jp/topics/top-picks']  # Crawl を開始する URL の List

    def parse(self, response):
        """
        Topics 一覧から個々の Topics への Link を抜き出してたどる
        """
        for url in response.css('ul.newsFeed_list a::attr("href")').re(r'/pickup/\d+$'):
            yield response.follow(url, self.parse_topics)

    def parse_topics(self, response):
        """
        Topics の Page から Title と本文を抜き出す。
        """
        item = Headline()
        item['title'] = response.css('.sc-dLxkki::text').get()  # Title
        item['body'] = response.css('.highLightSearchTarget').xpath('string()').get()  # 本文
        yield item  # Item を yield して、Data を抽出する。
