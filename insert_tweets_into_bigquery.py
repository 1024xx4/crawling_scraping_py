import os
import logging
import json
import html
from datetime import timezone
from io import BytesIO

import tweepy
from google.cloud import bigquery

# 環境変数から認証情報を取得する
TWITTER_API_KEY = os.environ['TWITTER_API_KEY']
TWITTER_API_kEY_SECRET = os.environ['TWITTER_API_KEY_SECRET']
TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']


def main():
    """
    Main となる処理。
    :return:
    """
    # BigQuery の Client を作成し、Table を取得する
    client = bigquery.Client()
    table = get_or_create_table(client, 'twitter', 'tweets')
    # OAuthHandler object を作成し、認証情報を設定する。
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_kEY_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

    logging.info('Collecting tweets...')
    # OAuthHandler と StreamListener を指定して Stream object を取得する。
    # MyStreamListener の Constractor には BigQuery の Client と Table の参照を渡す。
    stream = tweepy.Stream(auth, MyStreamListener(client, table.reference))
    # 公開されている Tweet を Sampling した Stream を受信する。
    # 言語を指定していないので、あらゆる言語の Tweet を取得できる。
    stream.sample()


def get_or_create_table(client: bigquery.Client, dataset_id: str, table_id: str) -> bigquery.Table:
    """
    BigQuery の Dataset と Table を作成する。既に存在する場合は取得する。
    :param client: bigquery.Client
    :param dataset_id: str
    :param table_id: str
    :return: bigquery.Table
    """
    logging.info(f'Creating dataset {dataset_id} if not exists...')
    dataset = client.create_dataset(dataset_id, exists_ok=True)  # Dataset を作成または取得する。

    logging.info(f'Creating table {dataset_id}.{table_id} if not exists...')
    table_ref = dataset.table(table_id)
    return client.create_table(  # Table を作成または取得する
        bigquery.Table(table_ref, schema=[bigquery.SchemaField('id', 'string', description='TweetのID'),
                                          bigquery.SchemaField('lang', 'string', description='Tweetの言語'),
                                          bigquery.SchemaField('screen_name', 'string', description='User名'),
                                          bigquery.SchemaField('text', 'string', description='Tweetの本文'),
                                          bigquery.SchemaField('created_at', 'timestamp', description='Tweetの日時'),
                                          ]),
        exists_ok=True
    )


class MyStreamListener(tweepy.StreamListener):
    """
    Streaming API で取得した tweet を処理するための Class.
    """

    def __init__(self, client: bigquery.Client, table_ref: bigquery.TableReference):
        self.client = client
        self.table_ref = table_ref
        self.status_list = []  # BigQuery にまとめて Load する Status object を留めておく List.
        self.num_loaded = 0  # BigQuery に Load した行数。
        super().__init__()  # 親 Class の__init__() を呼び出す

    def on_status(self, status: tweepy.Status):
        """
        Tweet を受信したときに呼び出される Method. 引数は Tweet を表す Status objet
        :param status: tweepy.Status
        :return:
        """
        self.status_list.append(status)  # Status object を status_list に追加する。

        if len(self.status_list) >= 500:
            # status_list に 500件溜まったら BigQuery に Load する。
            self.load_tweets_info_bigquery()

            # num_loaded を増やして、status_list を空にする。
            self.num_loaded += len(self.status_list)
            self.status_list = []
            logging.info(f'{self.num_loaded} rows loaded.')

            # 料金が高額にならないように、5000件を Load したら False を返して終了する。
            # 継続的に Load したいときには次の２行を Comment out する。
            if self.num_loaded >= 5000:
                return False

    def load_tweets_info_bigquery(self):
        """
        Tweet data を BigQuery に Load する。
        :return:
        """
        # Tweet の Status object の List を改行区切りの JSON（jSON Lines 形式）文字列に変換する。
        # 改行区切りの JSON 文字列は BytesIO（Memory 上の File object）に書き込む。
        bio = BytesIO()
        for status in self.status_list:
            json_text = json.dumps({
                'id': status.id_str,
                'lang': status.lang,
                'screen_name': status.author.screen_name,
                'text': html.unescape(status.text),  # text には文字参照が含まれていることがあるので元に戻す。
                # datatime object を UTC の POSIX Timestamp に変換する。
                'created_at': status.created_at.replace(tzinfo=timezone.utc).timestamp(),
            }, ensure_ascii=False)  # ensure_ascii = False は絵文字などの文字化けを回避する Hack
            bio.write(json_text.encode('utf-8'))
            bio.write(b'\n')

        bio.seek(0)  # 先頭から読み込めるよう BytesIO を先頭に Seek する。

        # BigQuery に Data を Load する Job を実行する。
        logging.info('Loading tweets into table...')
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON)  # JSON Lines 形式を指定
        job = self.client.load_table_from_file(bio, self.table_ref, job_config=job_config)
        job.result()  # Job の完了を待つ。Error を無視する場合は待たなくても良い。


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # INFO Level 以上の Log を出力する。
    main()
