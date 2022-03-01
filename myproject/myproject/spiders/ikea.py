from scrapy.spiders import SitemapSpider


class IkeaSpider(SitemapSpider):
    name = 'ikea'
    allowed_domains = ['www.ikea.com']
    # この設定がないと 504 Gateway Time-out となることがある。
    # setting.py で USER_AGENT を設定している場合、この設定は削除してよい。
    custom_settings = {
        'USER_AGENT': 'keabot',
    }
    # XML Sitemap の URL List.
    # robots.txt の URL を指定すると、Sitemap Directive から XML Sitemap の URL を取得する。
    sitemap_urls = [
        'https://www.ikea.com/robots.txt',
    ]
    # Sitemap index からたどる Sitemap URL の正規表現の List.
    # この List の正規表現に match する URL の Sitemap のみをたどる
    # sitemap_follow を指定しない場合は、すべての Sitemap をたどる
    sitemap_follow = [
        r'prod-ja-JP',
    ]
    # Sitemap に含まれる URL を処理する Callback関数を指定する Rule の List.
    # sitemap_rules を指定しない場合はすべての URL の Callback関数は`parse` method となる
    sitemap_rules = [
        (r'/products/', 'parse_product')
    ]

    def parse_product(self, response):
        # 製品 Page から製品の情報を抜き出す。
        yield {
            'url': response.url,  # URL
            'name': response.css('#name::text').get().strip(),  # 名前
            'type': response.css('#type::text').get().strip(),  # 種類
            # 価格。円記号と数値の間に \xa0（HTML では &nbsp:）が含まれているのでこれを space に置き換える。
            'price': response.css('#price1::text').re_first('[\S\xa0]+').replace('\xa0', ''),
        }
