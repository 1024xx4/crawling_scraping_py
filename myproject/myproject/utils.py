import logging
from typing import Tuple

import lxml.html
import readability

# readability-lxml の DEBUG/INFO の Level が Log を表示しないようにする。
# Spider 実行時に readability-lxml の Log が大量に表示されて、Log が見づらくなるのを防ぐため。
logging.getLogger('readability.readability').setLevel(logging.WARNING)


def get_content(html: str) -> Tuple[str, str]:
    """
    HTML の文字列から（Title, 本文）の Tuple を取得する
    """
    document = readability.Document(html)
    content_html = document.summary()
    # HTML tag を除去して本文の Text のみを取得する。
    content_text = lxml.html.fromstring(content_html).text_content().strip()
    short_title = document.short_title()

    return short_title, content_text
