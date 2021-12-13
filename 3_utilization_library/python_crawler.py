# Python による Crawler
# Requests で Web page を取得
# lxml で Scraping
# PyMong で MongoDB に Data 保存

from typing import Iterator
import requests
import lxml.html


def main():
    """
    Crawler の main 処理
    """
    session = requests.Session()
    response = requests.get('https://gihyo.jp/dp')
    urls = scrape_list_page(response)
    for url in urls:
        response = session.get(url)
        ebook = scrape_detail_page(response)
        print(ebook)
        break


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
        'title': html.cssselect('#bookTitle')[0].text_content(),
        'price': html.cssselect('.buy')[0].text,
        'content': [h3.text_content() for h3 in html.cssselect('#content > h3')],
    }
    return ebook


if __name__ == '__main__':
    main()
