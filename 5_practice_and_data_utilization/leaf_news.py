import os
import logging

import mechanicalsoup

LEAF_LOGIN = os.environ['LEAF_LOGIN']
LEAF_PASSWORD = os.environ['LEAF_PASSWORD']


def main():
    browser = mechanicalsoup.StatefulBrowser()

    # お知らせ Page を開く
    logging.info('Navigating...')
    browser.open('https://leaf-of-worker-roster.herokuapp.com/news')

    # Signin page に Redirect されていることを確認する
    assert '/sign_in' in browser.get_url()

    # Signin Form （id="new_user" の要素内にある form）を埋める
    browser.select_form('#new_user')
    browser['user[email]'] = LEAF_LOGIN  # name="user[email]" という入力 Box を埋める。
    browser['user[password]'] = LEAF_PASSWORD  # name="user[password]" を埋める。

    # Form を送信する
    logging.info('Signing in...')
    browser.submit_selected()

    # Signin に失敗する場合は、下記 Comment を外して確認する
    # print(browser.get_current_page().prettify())  # 現在の Page の HTML Source を表示する

    # お知らせ page が表示されていることを確認する
    assert 'お知らせ' in browser.get_current_page().title.string

    # 各お知らせの Title と URL を表示する。
    tds = []
    for td in browser.get_current_page().select('.table tr td:first-child'):
        tds.append(td.text)

    urls = []
    for a in browser.get_current_page().select('.table tr td a.btn-info'):
        urls.append(browser.absolute_url(a.get('href')))  # href 属性の値は相対 URL なので、絶対 URL に変換する。

    for td, a in zip(tds, urls):
        print(td, a)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # INFO Level 以上の Log を出力する
    main()
