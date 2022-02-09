import os

import tweepy

# 環境変数から認証情報を取得する。
TWITTER_API_KEY = os.environ['TWITTER_API_KEY']
TWITTER_API_SECRET_KEY = os.environ['TWITTER_API_SECRET_KEY']
TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']


def main():
    """
    Main となる処理
    :return:
    """
    # OAuthHandler object を作成し、認証情報を設定する。
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

    # OAuthHandler と StreamListener を指定して Stream object を取得する。
    stream = tweepy.Stream(auth, MyStreamListener())

    # 公開されている Tweet を Sampling した Stream を受信する。
    # Keyword 引数 languages で、日本語の Tweet のみに絞り込む。
    stream.sample(languages=['ja'])


class MyStreamListener(tweepy.StreamListener):
    """
    Streaming API で取得した Tweet を処理するための Class
    """

    def on_status(self, status: tweepy.Status):
        """
        Tweet を受信したときに呼び出される Method. 引数は Tweet を表す Status object
        :param status:
        :return: str
        """
        print(f'@{status.author.screen_name}', status.text)


if __name__ == '__main__':
    main()
