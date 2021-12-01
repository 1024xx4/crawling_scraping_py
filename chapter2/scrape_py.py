import re
from html import unescape
from urllib.parse import urljoin

# dp.html file の中身を変数 html に格納する。
with open('dp.html') as f:
    html = f.read()

# re.findall() を使用して、書籍１冊に相当する部分の HTML を取得する。
for partial_html in re.findall(r'<a itemprop="url".*?</ul>\s*</a></li>', html, re.DOTALL):
    # 書籍の URL は、itemprop="url" 属性を持つ a tag から取得する。
    url = re.search(r'<a itemprop="url" href="(.*?)"', partial_html).group(1)
    url = urljoin('https://gihyo.jp/', url) # 相対 URL を絶対 URL に変換する。

    title = re.search(r'<p itemprop="name".*?</p>', partial_html).group(0) # まずは p 要素全体を取得する
    title = title.replace('<br/>', ' ') # str.replace()で、<br/> tag を Space に置き換える。
    title = re.sub(r'<.*?>', '', title) # Tag を取り除く
    title = unescape(title) # 文字参照ｇ含まれている場合は元に戻す。

    print(url, title)