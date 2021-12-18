# Python による Crawler
# Requests で Web page を取得
# lxml で Scraping
# PyMong で MongoDB に Data 保存

import re
import time
from typing import Iterator
import requests
import lxml.html
from pymongo import MongoClient


def main():
    """
    Crawler の main 処理
    """
    client = MongoClient('localhost', 27017)  # localhost の MongoDB に接続する。
    collection = client.scraping.ebooks  # scraping Database の ebooks Collection を得る。
    collection.create_index('key', unique=True)  # Data を一意に識別する key を格納する key field に unique な index を作成する。

    session = requests.Session()
    response = requests.get('https://gihyo.jp/dp')  # 一覧 Page を取得する。
    urls = scrape_list_page(response)  # 詳細 page の URL 一覧を得る。
    for url in urls:
        key = extract_key(url)  # URL から key を取得する

        ebook = collection.find_one({'key': key})  # MongoDB から key に該当する Data を探す。

        if not ebook:  # MongoDB に存在しない場合だけ、詳細 Page を crawl する。
            time.sleep(1)
            response = session.get(url)
            ebook = scrape_detail_page(response)
            collection.insert_one(ebook)  # 電子書籍の情報を MongoDB に保存する。

        print(ebook)  # 電子書籍の上表を表示する


def scrape_list_page(response: requests.Response) -> Iterator[str]:
    """
    一覧 Page の Response から詳細 Page の URL を抜き出す Generator iterator 関数
    :param response:
    :return: yield 文で Generator iterator の要素
    """
    html = lxml.html.fromstring(response.text)
    html.make_links_absolute(response.url)

    for a in html.cssselect('#listBook > li > a[itemprop="url"]'):
        url = a.get('href')
        yield url


def scrape_detail_page(response: requests.Response) -> dict:
    """
    詳細 Page の Response から電子書籍の情報を dict で取得する。
    :param response:
    :return: dict
    """
    html = lxml.html.fromstring(response.text)
    ebook = {
        'url': response.url,
        'key': extract_key(response.url),  # URL から抜き出した key
        'title': html.cssselect('#bookTitle')[0].text_content(),  # Title
        'price': html.cssselect('.buy')[0].text.strip(),  # 価格（strip() で前後の空白を削除）
        'content': [normalize_spaces(h3.text_content()) for h3 in html.cssselect('#content > h3')],  # 目次
    }
    return ebook  # dict を返す。


def extract_key(url: str) -> str:
    """
    URL から key （URL の末尾の ISBN）を抜き出す。
    :param url:
    :return: str
    """
    m = re.search(r'/([^/]+)$', url)  # 最後の / から文字列末尾までを正規表現で取得。
    return m.group(1)


def normalize_spaces(s: str) -> str:
    """
    連続する空白を１つの Space に置き換え、前後の空白を削除した新しい文字列を取得する。
    :param s:
    :return: str
    """
    return re.sub(r'\s+', ' ', s).strip()


if __name__ == '__main__':
    main()
