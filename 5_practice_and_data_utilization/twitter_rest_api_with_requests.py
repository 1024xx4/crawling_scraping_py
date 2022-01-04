import os

from requests_oauthlib import OAuth1Session

TWITTER_API_KEY = os.environ['TWITTER_API_KEY']
TWITTER_API_SECRET_KEY = os.environ['TWITTER_API_SECRET_KEY']
TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

# 認証情報を使って OAuth1Session object を得る。
twitter = OAuth1Session(TWITTER_API_KEY, client_secret=TWITTER_API_SECRET_KEY, resource_owner_key=TWITTER_ACCESS_TOKEN, resource_owner_secret=TWITTER_ACCESS_TOKEN_SECRET)

# User の Timeline を取得する。
response = twitter.get('https://api.twitter.com/1.1/statuses/home_timeline.json')

# API の Response は JOSN 形式の文字列なので、response.json() で Purse して list を取得できる。
# status は tweet（Twitter API では Status と呼ばれる）を表す dict。
for status in response.json():
    print('@' + status['user']['screen_name'], status['text']) # User 名と tweet を表示する