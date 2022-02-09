import os

import tweepy

# 環境変数から認証情報を取得する。
TWITTER_API_KEY = os.environ['TWITTER_API_KEY']
TWITTER_API_SECRET_KEY = os.environ['TWITTER_API_SECRET_KEY']
TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

# 認証情報を設定する
auth = tweepy.OAuthHandler(consumer_key=TWITTER_API_KEY, consumer_secret=TWITTER_API_SECRET_KEY)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth) # API Client を取得する。
public_tweets = api.home_timeline() # User の Timeline を取得する。
for status in public_tweets:
    print(f'@{status.user.screen_name}', status.text) # User 名と tweet を表示する。