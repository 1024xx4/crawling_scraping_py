import scrapy

from myproject.items import Page
from myproject.utils import get_content


class BroadSpider(scrapy.Spider):
    name = 'broad'
    start_urls = ['https://b.hatena.ne.jp/entrylist/all']

    def parse(self, response):
        """
        はてなブックマークの新着 Entry page を parse する。
        """
        # 個別の Web page への Link をたどる。
        for url in response.css('.entrylist-contents-title > a::attr("href")').getall():
            # parse_page() method を Callback関数として指定する。
            yield scrapy.Request(url, callback=self.parse_page)

        # page= の値が１桁である間のみ「次の20件」の Link をたどる（最大９page まで）。
        url_more = response.css('.entrylist-readmore > a::attr("href")').re_first(r'.*\?page=\d{1}$')
        if url_more:
            yield response.follow(url_more)

    def parse_page(self, response):
        """
        個別の Web page を parse する。
        """
        # utils.py に定義した get_content()関数で Title と本文を抽出する。
        title, content = get_content(response.text)
        # Page object を作成して yield する。
        yield Page(url=response.url, title=title, content=content)
