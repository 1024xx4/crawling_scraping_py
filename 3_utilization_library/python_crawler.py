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
    response = requests.get('https://gihyo.jp/dp')
    urls = scrape_list_page(response)
    for url in urls:
        print(url)


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

if __name__ == '__main__':
    main()