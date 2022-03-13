# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from pymongo import MongoClient

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

# class MongoPipeline:
#     """
#     Spider の開始時に MongoDB に接続する
#     """
#     self.client = MongoClient('localhost', 27017)  # Host と port を指定して Client を作成。
#     self.db = self.client['scraping-book']  # scraping-book Database を取得
#     self.collection = self.db['items']  # items collection を取得。
#
#     def close_spider(self, spider):
#         """
#         Spider の修了時に MongoDB への接続を切断する。
#         """
#         self.client.close()
#
#     def process_item(self, item, spider):
#         """
#         Item を Collection に追加する。
#         """
#         # insert_one()の引数は書き換えられるので、Copy した dict を渡す。
#         self.collection.insert_one(dict(item))
#         return item
