import mechanicalsoup

browser = mechanicalsoup.StatefulBrowser()  # StatefulBrowser object を作成する。
browser.open('https://www.google.co.jp/')  # open() method で Google の Top page を開く。

# 検索語を入力して送信する。
browser.select_form('form[action="/search"]')  # 検索 Form を選択する。
browser['q'] = 'Python'  # 選択した Form にある name="q" の入力 Box に検索語を入力する。
browser.submit_selected()  # 選択した Form を送信する。

# 検索結果の Title と URL を抽出して表示する。
page = browser.get_current_page()  # 現在の Page の BeautifulSoup object を取得する。
for a in page.select('div > div > div > div > a > h3'):  # CSS Selector に Match する要素（Tag object）の List を取得する。
    print(a.text)
    print(browser.absolute_url(a.get('href')))  # Link の URL を絶対 URL に変化して表示する。
