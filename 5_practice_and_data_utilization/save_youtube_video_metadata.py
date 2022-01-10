import os
import logging
from typing import Iterator, List

from apiclient.discovery import build
from pymongo import MongoClient, ReplaceOne, DESCENDING
from pymongo.collection import Collection

YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']  # 環境変数から API Key を取得する。
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)  # 不要な Log を出力しないよう設定。


def main():
    """
    Main の処理
    :return:
    """
    mongo_client = MongoClient('localhost27017')  # MongoDB の Client object を作成する。
    collection = mongo_client.youtube.videos  # Youtube の Database の videos collection を取得する。

    # 動画を検索し、Page 単位で Item の List を保存する。
    for items_per_page in search_videos('手芸'):
        save_to_mongodb(collection, items_per_page)

    show_top_videos(collection)  # View 数の多い動画を表示する。


def search_videos(query: str, max_pages: int = 5) -> Iterator[List[dict]]:
    """
    引数 query で動画を検索して、Page 単位で Item の List を yield する。
    最大 max_page まで検索する。
    :param query: Str
    :param max_pages: Int
    :return: Iterator[List[dict]]
    """
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)  # YouTube の API Client を組み立てる。

    # search.list method で最初の Page を取得するための Request を得る。
    search_request = youtube.search().list(
        part='id',  # search.list では動画 ID だけを取得できれば良い。
        q=query,
        type='video',
        maxResults=50,  # １page あたり最大50件の動画を取得する。
    )

    # Request が有効、かつ Page 数が max_pages 以内の間、繰り返す。
    # 実際にはもっと多くの Page を取得してもよい。
    i = 0
    while search_request and i < max_pages:
        search_response = search_request.execute()  # Request を送信する。
        video_ids = [item['id']['videoId'] for item in search_response['items']]  # 動画 ID の List を得る。

        # video.list method で動画の詳細な情報を得る。
        videos_response = youtube.videos().list(
            part='snippet, statistics',
            id=','.join(video_ids)
        ).execute()

        yield videos_response['items']  # 現在の Page に対応する Item の List を yield する。

        # list_next() method で次の Page を取得するための Request（次の Page がない場合は None）を得る。
        search_request = youtube.search().list_next(search_request, search_response)
        i += 1


def save_to_mongodb(collection: Collection, items: List[dict]):
    """
    MongoDB に保存する前に、後で使いやすいように Item を書き換える。
    :param collection: Collection
    :param items: List[dict]
    """
    for item in items:
        item['_id'] = item['id']  # 各 Item の id 属性を MongoDB の _id 属性として使う。

        # statistics に含まれる viewCount property などの値が文字列になっているので、数値に変換する。
        for key, value in item['statistics'].items():
            item['statistics'][key] = int(value)

    # 単純に collection.insert_many() を使うと _id が重複した場合に Error になる。
    # 代わりに collection.bulk_write() で複数の upsert（insert or update）をまとめて行なう。
    operations = [ReplaceOne({'_id': item['_id']}, item, upsert=True) for item in items]
    result = collection.bulk_write(operations)
    logging.info(f'Upserted {result.upserted_count} documents.')


def show_top_videos(collection: Collection):
    """
    MongoDB の Collection 内で View 数の上位５件を表示する。
    :param collection: Collection
    """
    for item in collection.find().sort('statistics.viewCount', DESCENDING).limit(5):
        print(items['statistics']['viewCount'], item['snippet']['title'])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # INFO level 異常の Log を出力する。
    main()
