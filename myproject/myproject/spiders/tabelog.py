from myproject.items import Restaurant
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TabelogSpider(CrawlSpider):
    name = 'tabelog'
    allowed_domains = ['tabelog.com']
    start_urls = [
        # 東京の昼の Ranking の URL
        # 普通に Web site を見ていると、多くの Query parameter がついているが、
        # Pager の Link を見ると、値が 0 の Query parameter は省略できることがわかる。
        'https://tabelog.com/tokyo/rstLst/lunch/?LstCosT=2&RdoCosTp=1',
    ]

    rules = [
        Rule(LinkExtractor(allow=r'/\w+/rstLst/lunch/\d/')),
        Rule(LinkExtractor(allow=r'/\w+/A\d+/A\d+/\d+/$'), callback='parse_restaurant'),
    ]

    def parse_restaurant(self, response):
        """
        Restaurant の詳細 page を parse する。
        """
        latitude, longitude = response.css('img.js-map-lazyload::attr("data-original")').re(
            r'markers=.*?%7C([\d.]+),([\d]+)')

        item = Restaurant(
            name=response.css('.display-name').xpath('string()').get().strip(),
            address=response.css('.rstinfo-table__address').xpath('string()').get().strip(),
            latitude=latitude,
            longitude=longitude,
            station=response.css('dt:contains("最寄り駅")+ dd span::text').get(),
            score=response.css('[rel="v:rating"] span::text').get(),
        )

        yield item
