# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Headline(scrapy.Item):
    """
    News の HeadLine を表す Item.
    """

    title = scrapy.Field()
    body = scrapy.Field()


class Restaurant(scrapy.Item):
    """
    食べログの Restaurant情報。
    """

    name = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    station = scrapy.Field()
    score = scrapy.Field()


class Page(scrapy.Item):
    """
    Web page.
    """

    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

    def __repr__(self):
        """
        Log への出力時に長くなり過ぎないよう、content を省略する。
        """
        p = Page(self)  # この Page を複製した Page を得る。
        if len(p['content']) > 100:
            p['content'] = p['content'][:100] + '...'  # 100文字より長い場合は省略する。

        return super(Page, p).__repr__()  # 複製した Page の文字列表現を返す。
