import scrapy


class BlogSpider(scrapy.Spider):
    name = 'blogspider'  # Spider の名前
    start_urls = ['https://www.zyte.com/blog/']  # Crawl を開始する URL の List.

    def parse(self, response):
        """
        Page から投稿の Title をすべて抜き出し、次の Page への Link があればたどる
        """
        # Page から投稿の Title をすべて抜き出す。
        for title in response.css('a.oxy-post-title'):
            yield {'title': title.css('a ::text').get()}

        # 次の Page（OLDER POST）への Link があればたどる。
        for next_page in response.css('a.next page-numbers"'):
            yield response.follow(next_page, self.parse)
