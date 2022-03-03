# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class MyprojectPipeline:
    def process_item(self, item, spider):
        return item


class ValidationPipeline:
    """
    Item を検証する Pipeline
    """

    def process_item(self, item, spider):
        if not item['title']:
            # title Field が取得できていない場合は破棄する。
            # DropItem() の引数は破棄する理由を表す Message.
            raise DropItem('Missing title')

        return item  # title Field が正しく取得できている場合。
