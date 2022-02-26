import lxml.html
from pymongo import MongoClient

client = MongoClient('localhost', 27017) # MongoDB に接続
db = client.scraping # `scraping` database を取得 ※ 無ければ作成
collection = db.books # `books` collection を取得 ※ 無ければ作成

collection.delete_many({}) # Script の実行毎に Collection の Document をすべて削除。

tree = lxml.html.parse('../5_practice_and_data_utilization/dp.html') # HTML file の読み込み
html = tree.getroot() # HtmlElement object の取得
html.make_links_absolute('https://gihyo.jp/') # 引数の URL を基準として、すべての a 要素の href 属性を絶対 URL に変換

for a in html.cssselect('#listBook > li > a[itemprop="url"]'):
    url = a.get('href') # a 要素の href 属性から書籍の URL を取得
    p = a.cssselect('p[itemprop="name"]')[0] # itemprop="name" という属性を持つ p 要素を取得
    title = p.text_content() # 取得した p 要素から書籍の Title を取得 ※wbr 要素などを含まないように text_content() method を使用

    collection.insert_one({'url': url, 'title': title}) # 書籍の URL, Title を MongoDB に保存

# MongoDB の `books` collection の Document を _id 順に sort して出力
for link in collection.find().sort('_id'):
    print(link['_id'], link['url'], link['title'])
