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
