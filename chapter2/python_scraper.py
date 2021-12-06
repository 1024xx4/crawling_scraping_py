import csv
from typing import List  # 型 hint のために import

import requests
import lxml.html


def main():
    """
    Main の処理。fetch(), scrape(), save() の３つの関数を呼び出す。
    """

    url = 'https://gihyo.jp/dp'
    html = fetch(url)
    books = scrape(html, url)
    save('dump/books.csv', books)


def fetch(url: str) -> str:
    """
    :param url:
        引数 url で与えられた URL の Web page を取得する。
        Web page の encoding は Content-Type header から取得する。
    :return:str 型の HTML
    """

    r = requests.get(url)
    return r.text


def scrape(html: str, base_url: str) -> List[dict]:
    """

    :param html: 与えられた HTML から正規表現で書籍の情報を抜き出す。
    :param base_url: 絶対 URL に変換する際の基準となる URL を指定する。
    :return: 書籍（dict）の List
    """

    books = []
    html = lxml.html.fromstring(html)
    html.make_links_absolute(base_url)  # すべての a 要をの href 属性を絶対 URL に変換する。

    for a in html.cssselect('#listBook > li > a[itemprop="url"]'):
        url = a.get('href')

        p = a.cssselect('p[itemprop="name"]')[0]
        title = p.text_content()

        books.append({'url': url, 'title': title})

    return books


def save(file_path: str, books: List[dict]):
    """
    引数 books で与えられた書籍の List を CSV 形式の File に保存する。
    :param file_path: 保存先の File path
    :param books: 与える書籍の List
    :return: なし
    """

    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, ['url', 'title'])
        writer.writeheader()
        writer.writerows(books)


if __name__ == '__main__':
    main()
