import os
from urllib.parse import urlencode

import scrapy


class FlickrSpider(scrapy.Spider):
    name = 'flickr'
    # Files Pipeline で Download される画像File は allowed_domains に制限されないので、allowed_domains に 'staticflickr.com'を
    # 追加する必要はない。
    allowed_domains = ['api.flickr.com']

    # Keyword引数で Spider 引数の値を受け取る。
    def __init__(self, text='sushi'):
        super().__init__()

        # 環境変数と Spider引数の値を使って start_urls を組み立てる。
        # urlencode()関数は、引数に指定した dict の key と値を URL encode して「key1=value1&key2=value2」という形式の文字列を返す
        self.start_urls = [
            'https://api.flickr.com/services/rest/?' + urlencode({
                'method': 'flickr.photos.search',
                'api_key': os.environ['FLICKR_API_KEY'],  # Flickr の API key は環境変数から取得。
                'text': text,
                'sort': 'relevance',
                'license': '4,5,9',
            }),
        ]

    def parse(self, response):
        """
        API の Response を parse して file_urls という Key を含む dict を yield する
        """
        for photo in response.css('photo'):
            yield {'file_urls': [flickr_photo_url(photo)]}


def flickr_photo_url(photo: scrapy.Selector) -> str:
    """
    Flickr の写真の URL を組み立てる。
    参考: https://www.flicker.com/services/api/misc.urls.html
    """
    attrib = dict(photo.attrib)  # photo要素の属性を dict として取得
    attrib['size'] = 'b'  # Size の値を追加
    return 'https://farm{farm}.staticflickr.com/{server}/{id}_{secret}_{size}.jpg'.format(**attrib)
