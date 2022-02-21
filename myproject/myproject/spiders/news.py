import scrapy


class NewsSpider(scrapy.Spider):
    name = 'news'  # Spider の名前
    allowed_domains = ['news.yahoo.co.jp']  # Crawl 対象とする Domain の List
    start_urls = ['https://news.yahoo.co.jp/topics/top-picks']  # Crawl を開始する URL の List

    def parse(self, response):
        """
        Top page の Topics一覧から個々の Topics への Link を抜き出して表示する
        """
        print(response.css('ul.newsFeed_list a::attr("href")').getall())
