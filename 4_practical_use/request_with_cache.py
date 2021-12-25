import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache

session = requests.Session()
# session を wrap した cached_session を作る。
# Cache は、File として .webcache Directory 内に保存する。
cached_session = CacheControl(session, cache=FileCache('.webcache'))

response = cached_session.get('https://docs.python.org/3')  # 通常の Session と同様に使用する。

# response.from_cache 属性で Cache から取得された Response かどうか取得できる。
print(f'from_cache: {response.from_cache}')  # 初回は False。２回目以降は True。

print(f'status_code: {response.status_code}')  # Status code を表示。

print(response.text)  # Response body を表示。
