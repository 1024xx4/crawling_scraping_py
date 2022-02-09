import os

from apiclient.discovery import build

YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY'] # 環境変数から API Key を取得する

# YouTube の API Client を組み立てる。
# build()関数の第１引数には API 名を、
# 第２引数には API の Version を指定し、
# Keyword 引数 developerKey で API Key を指定する。
# この関数は内部的に https://www.googleapis.com/discovery/v1/apis/youtube/v3/rest という URL に access し、API resource や Method の情報を取得する。
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Keyword 引数で引数を指定し、search.list method で呼び出す。
# list() method で googleapiclient.http.HttpRequest object が得られ、execute() method を実行すると実際に HTTP request が送られて、API response が得られる。
search_response = youtube.search().list(
    part = 'snippet',
    q = '手芸',
    type = 'video',
).execute()

# search_response は API response の JSON を Perth した dict.
for item in search_response['items']:
    print(item['snippet']['title']) # 動画の Title を表示する