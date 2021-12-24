# Crawling・Scraping とは何か
## Crawler（クローラー）
Web page 上の情報を取得するための Program.  
<small>Spider（スパイダー）、Bot（ボット）などとも呼ばれる。</small>

## Crawler の利用 Case
- Google や Bing などの検索 Engine.
- RSS Reader
- SNS なで Web page を貼り付けた時に Page の Title や画像を自動的に表示させる。
## Crawler の活用 Idea
- 店舗の混雑状況を web page 上で Real time に提供する。  
  - 混雑状況がすぐにわかる。
  - 継続的に情報を取得し毎日１日時間おきに Web page の混雑状況を取得して Graph 化することで混雑する曜日や時間帯がわかってくる。
- 複数の Web site から情報を抜き出して、整理する  
  - 複数 Site から商品の価格を取得し比較することで最安値で商品の購入ができる。
- Open data （政府や自治体、企業などが自由な利用を認めて公開する Data)の取得。
- 大学や企業での研究で、Web 上の Data を分析する。  
  ※ Data set が公開されていない場合も Data の収集が可能になる。

## Crawler を利用するにあたっての注意
高速に Web page を取得できるため、無計画に取得すると 対象の Web page を提供する Server に負荷をかけすぎる。  
- 自身の、Request で専有してしまい他者や Crawler が 対象の Web page に Access できなくなる。
- Server 側に転送量の制限があったり、従量課金制で多額の費用を発生させてしまう。

## Crawling と Scraping
### Crawling（クローリング）
Crawler を使って Data を収集すること。  
Web page の Hyper link をたどって次々に Web page を Download する作業。
### Scraping（スクレイピング）
Web page から必要な情報を抜き出す作業。  
Download した Web page から必要な情報を抜き出す作業。

# Wget による Crawling
## Wget とは
**GNU Wget(Wget)**とは、HTTP 通信や、FTP 通信を使用して、Server から File や Contents を Download するための Software(Downloader)。  
Command line から簡単に使用できる。
### Wget の特徴
Crawling 機能がある。複数の File を一度に Download したり、Web page の Link をたどって複数の Contents を Download したりできる。

### Wget でよく使う Option
| Option                              | 説明                                                 |
|-------------------------------------|----------------------------------------------------|
| -V, -version                        | Wget の Version を表示する。                              |
| -h, --help                          | Help を表示する。                                        |
| -q, --quit                          | 進捗状況などを表示しない。                                      |
| -O *file*, --output-document=*file* | *file* に保存する。                                      |
| -c, --continue                      | 前回の続きから File の Download を再開する。                     |
| -r, --recursive                     | Link をたどって再帰的に Download する。                        |
| -l *depth*, --level=*depth*         | 再帰的に Download するときに Link をたどる深さを *depth* に制限する。    |
| -w *seconds*, --wait=*seconds*      | 再帰的に Download するときに Download 感覚として *seconds* 秒空ける。 |
| -np, --no-parent                    | 再帰的に Download するときに親 Directory を Crawl しない。        |
| -l *list*, --include *list*         | 再帰的に Download するときに *list*に含まれる Directory のみをたどる。  |
| -N, --timestamping                  | File が更新されているときのみ Download する。                     |
| -m, --mirror                        | Mirroring 用の Option を有効化する。                        |
| --restrict-file-names=nocontrol     | URL に日本語が含まれる場合に、日本語の File 名で保存する。                 |

# Scraping に役立つ Unix Command
HTML file から目的の Data を抜き出すために
- Unix command
- 正規表現
が必要。

## Unix command
- 一つ一つは単純な機能しかないが、複数を組み合わせることで複雑な Text 処理が行なえる。
- Scraping だけではなく、Data 集計などでも役立つ。

## 標準 Stream
標準入力、標準出力、標準 Error 出力の３つの総称。
### 標準入力
Command が入力を受け取る元
### 標準出力
結果を出力する先
### 標準 Error 出力
Error などの補足情報を出力する先

## Redirect
標準 Stream を Console 画面ではなく、File から入力したり File に出力すること。

## Pipe(パイプ)
ある Command の標準出力を他の Command の標準入力に渡すこと。

## Text 処理のための Unix Command 
### cat
引数で与えた File を出力する
```
yakei_kobe.csv を出力する
$ cat yakei_kobe.csv
```

### grep
- 引数で指定した文字列を含む行を抜き出す
- 引数で指定した正規表現に Match する行を抜き出す。
```
yakei_kobe.csv から「六甲」という文字列を含む行のみ出力する
$ cat yakei_kobe.csv | grep 六甲
```

### cut
特定の文字で区切られた Text の一部の列を抜き出す。

| Option | 説明             |
|--------|----------------|
| -d     | 区切り文字の指定       |
| -f     | 列番号の指定（複数指定可能） |

```
yakei_kobe.csv から 「,（Comma）」で区切った１，２列目の Data を出力する。
$ cat yakei_kobe.csv | cut -d , -f 1,2
```
### sed
特定の条件に Match する行を置き換えたり、削除したりできる。引数に  
**'s/検索する正規表現/置換する文字列/Option'**  
で正規表現に Match する箇所を置換する文字列に置き換えて出力する。

| 末尾の Option | 説明                              |
|------------|---------------------------------|
| g          | １行に検索する正規表現が複数回出現する場合でもすべて置換する。 |

```
yakei_kobe.csv file の「,」を Space に置き換えて出力
$ cat yakei_kobe.csv | sed '/s/,/ /g'
```

## 正規表現（Regular Expression）
特定の Pattern の文字列を表すための文字列表現。Pattern に Match する文字列を検索するために使用する。
Pattern を表すために Meta 文字と呼ばれる記号を使う。

### 正規表現の規格
| 規格                                               | 説明                                                      |
|--------------------------------------------------|---------------------------------------------------------|
| POSIX の基本正規表現 （BRE: Basic Regular Expressions）   | grep や sed などの Unix command で標準て使用できる。                  |
| POSIX の拡張正規表現（ERE: Extended Regular Expressions） | BRE よりも表現力が高い。-E option をつけることで Unix command でも利用可能。    |
| Perl の正規表現                                       | ERE よりも強力で、様々な Pattern を表現できる。Python の正規表現もほぼ同じ正規表現になる。 |

### 正規表現の Meta 文字
| Meta 文字 | 説明                             |
|---------|--------------------------------|
| .       | 任意の１文字に Match                  |
| []      | []で囲まれた文字のいずれかに１文字に Match      |
| []内の -  | - で文字の範囲を表す。                   |
| []内の ^  | ^ を最初につけることで否定を表す。             |
| ^       | 行の先頭に Match                    |
| $       | 行の末尾に Match                    |
| *       | 直前の Pattern を０回以上繰り返す。         |
| +       | 直前の Pattern を１回以上繰り返す。         |
| ?       | 直前の Pattern を０回か１回繰り返す。        |
| {n}     | 直前の Pattern をちょうど n 回繰り返す。     |
| ()      | ()で囲まれた Pattern を Group 化する。   |
| ❘       | で区切られた Pattern のいずれかに Match する |

```
yakei_kobe.csv file 内で行頭に 1 という文字列がある行に Match
$ cat yakei_kobe.csv | grep -E '^1'

yakei_kobe.csv file 内で「,」に続く５文字の Spot 名がある行に Match
$cat yakei_kobe.csv | grep -E ',.{5}'
```

# Unix command による Crawling と Scraping について
## 強味
wget, grep sed などを利用して、手軽に Crawling と Scraping ができる
## 弱み
実用上は機能不足
### Crawling
たどる Link やその順序の制御
- Wget では、Directory 単位でしが制御できない。
- たどる順序の明示的な制御はできない。
- File を Download した時に何らかの処理も行なうことができない。
### Scraping
行指向になっていて、行単位になっていない Data を扱うのは苦手。

# Python で行なう Crawling & Scraping
## Merit
### 言語自体の特性
- 読みやすく、書きやすい。Program は他人に読まれることになるため、読みやすさは重要。
- 豊富な標準 Library が付属していて Install 後すぐに使用可能。
- 非同期処理の為の Framework や標準 Library があり手軽に使用可能。
### 強力な Third party library の存在
- lxml, Beautiful Soup という有名な Scraping library がある。
- Scrapy という強力な Crawling & Scraping Framework がある。
### Scraping 後のよりとの親和性
Crawling, Scraping で Data を取得した後の Data 分析に強力な Library がある。
NumPy, SciPy という数値計算や科学技術計算の Library を Base にした Data分析用がある。

| Library    | 説明                                                   |
|------------|------------------------------------------------------|
| pandas     | NumPy を Base として Data の前処理（欠損値の処理・正規化など）や集計を簡単に行なえる。 |
| matplotlib | 数値 Data を Graph で可視化                                 |

R と同様の分析が行なえる。

# Python で Web page を取得する
Third party library の Requests を使用する。
## Requests
HTTP header の追加や Basic 認証などの少し凝ったことを使用としても簡単に使用できる UI が用意されている。

| 関数        | 対応する HTTP Method |
|-----------|------------------|
| get()     | GET              |
| post()    | POST             |
| put()     | PUT              |
| patch()   | PATCH            |
| delete()  | DELETE           |
| head()    | HEAD             |
| options() | OPTIONS          |

### Response Object(requests.get で得られる Object)
- .text で str 型の文字列を得らえる。
- .content が .encoding で Decode されたものが出力される。
- .text で文字化けする場合、.encoding='encode' のように上書きすると指定した Encoding で Decode されて出力さる。
- Response body が圧縮されていても自動的に展開されるため、特に気にする必要はない。

## HTTP Request と Response
次の４つの要素から構成される。
- 開始行
- Header（省略可能）
- 空行（Header の終わりを表す）
- Body（省略可能）

実際に取得したい HTML は Response body に格納されていて、Response header がその補足情報となる。

### Session object
複数の Page を Crawl する倍に効果的
- HTTP header や Basic 認証などの設定を複数の Request で使いまわる。
- Cookie も自動的に引き継がれる。
- 同じ Web site に複数回 Request を送る時に TCP Connection の確率処理を省略でき、Performance 向上が期待できる。
- 相手の Server 側の負荷も軽減できる。

## 文字 Code
Server から受け取った HTTP response に含まれる Byte 列から元の文字列を復元するには**どの Encoding で Encode されたか**を知る必要がある。  
### 実際の Web site
- 管理者によって正しく指定されていない。
- 間違っている Encoding が指定されている。

ことがある。その場合、誤った Encoding で Decode すると文字化けを起こす。  
UTF-8 で Decode するのも１つの手だが日本語を含む多様な Site を Crawl する場合は、複数の Encoding が混在している可能性がある。

## Web page の Encoding を取得・推定する方法
| No  | 方法                                                                   | 補足                                                   |
|-----|----------------------------------------------------------------------|------------------------------------------------------|
| 1   | HTTP response の Content-Type header の charset で指定された Encoding を取得する。 | 正しくなかったり、charset が指定されていなかったりすることがある。                |
| 2   | HTTP response body の Byte列の特徴から Encoding を推定する。                      | 推定に使用する Response body が長いほど精度よく推定できるが、その分、処理時間が長くなる。 |
| 3   | HTML の meta tag で指定された Encoding を取得する。                               | １が正しく指定されている Site では、meta tag が指定されていないことがある。        |

## HTTP header から Encoding を取得する
Content-type header に charset が指定されていないと `r.encoding == 'ISO-8859-1'` となること。  
ISO-8859-1 は、ラテン文字のための Encoding なので、日本語の Web site を Decode すると文字化けする。

### ISO-8859-1 の対策
- UTF-8 とみなす。
- 他の方法を使用する。

## Response body の Byte 列から Encoding を推定する
Requests の Response object の apparent_encoding 属性で推定された Encoding が取得できるのでそれを利用する。

## meta tag から Encoding を取得する
meta tag の Encoding は Requests の機能では取得できないため正規表現を使って Encoding を取得する。

# Web page から Data を抜き出す
## 正規表現による Scraping
HTML を単純な文字列としてみなして必要な部分を抜き出す。文字列の特徴を捉えて Scraping できる
### Python の正規表現
標準 Library ```re``` module を利用する。

## HTML パーサーによる Scraping
HTML tag を解析して必要な部分を抜きだす。情報が適切に Markup されている Web page では、正規表現に比べて簡単かつ確実に必要とする部分を抜き出せる。
### XPath(XML Path Language)
XML の特定の要素を指定するための言語。

CSS Selector に比べて多機能で細かな条件が指定できる。

### CSS Selector
CSS を装飾する要素を指定するための表記方法。  
CSS や JS の使用経験があると馴染みやすい方法。

XPath に比べて簡潔に書ける。CSS Selector でざっくり抽出してから Python で細かく処理するということもできる。

## XPath と CSS Selector の書き方
| 探したい要素                        | XPath                                                                        | CSS selector                                                |
|-------------------------------|------------------------------------------------------------------------------|-------------------------------------------------------------|
| title                         | //title                                                                      | title                                                       |
| body の子孫の h1                  | //body//h1                                                                   | body h1                                                     |
| body の直接の子である h1              | //body/h1                                                                    | body > h1                                                   |
| body の任意の子要素                  | //body/*                                                                     | body > *                                                    |
| id が main                     | id("main") or //*[@id="main"]                                                | #main                                                       |
| class が active を含む li         | //li[@class and contains(concat('', normalize-space(@class), ''), 'active')] | li.active                                                   |
| type 属性が "text" の input       | //input[@type="text"]                                                        | input[type="text"]                                          |
| href 属性が"http://"で始まる a       | //a[starts-with(@href, "http://")]                                           | a[href^="http://"]                                          |
| src 属性が".jpg"で終わる img         | //img[ends-with(@src, ".jpg")] ※XPath 2.0 以降で使用可能                            | img[src$=".jpg"]                                            |
| 要素の子孫に"概要"という Text を含む h2     | //h2[contains(.,"概要")]                                                       | h2:contains("概要") ※cssselect の独自実装で CSS Selector の仕様には含まれない |
| 直下の Text が"概要"という Text である h2 | //h2[text()="概要"]                                                            | ※ CSS Selector では表現できない                                     |

## Library の XPath と CSS Selector の Support 状況
| Library          | 種類          | XPath | CSS Selector              |
|------------------|-------------|-------|---------------------------|
| ElementTree      | 標準 Library  | △     | ×                         |
| lxml + cssselect | Third party | 〇     | 〇（CSS3 Selector)          |
| Beautiful Soup   | Third party | ×     | △（CSS3 Selector の Subset） |
| pyquery          | Third party | ×     | 〇（CSS3 Selector）          |

### 開発者 Tool の活用
Browser の開発者 Tool で取得できる Xpath や CSS Selector を確認し、必要に応じて本質的なところだけ抽出したり使用する Selector を変更させながら活用すれば
Simple かつ変化に強くなる。

# Data の File 保存
## CSV形式
CSV（Comma-Separated Values）は、１Record を１行で表し、各行の値を Comma で区切った Text Format。  
２次元 Data の保存に向いている。

### CSV module の注意点
```csv.writer``` は、Default で Excel 互換の形式で出力し、Unix 系の OS においても File の改行 Code が CRLF になる。  
そのため、Unix 系の OS で ```open()```関数で普通に File を開くと、出力時に改行 Code が LF に自動変換されてしまうので、自動変換を抑制する為に ```open()```
関数で File を開く際は、```newline=''```を指定する。

## CSV / TSV file の Encoding
Unix 系 OS の Default encoding は、UTF-8。
Python で File を開いて保存する場合も ```encoding=''``` を指定しないと UTF-8 で保存される。  
Excel で開くと文字化けするので注意が必要になる。

### Excel における CSV / TSV
| Encoding         | Encoding の値 | 特徴                                                                   |
|------------------|-------------|----------------------------------------------------------------------|
| UTF-8            | 'utf-8'     | Unicode の文字を使用できるが Excel では文字化けする。                                   |
| UTF-8（BOM 付き）    | 'utf-8-sig' | Unicode の文字を使用できるが macOS 版 Excel では文字化けする                            |
| UTF-16           | 'utf-16'    | Unicode の文字を使用できるが Comma で区切られた CSV File を Excel で開いたときに列が正しく分割されない。 |
| Shift_JIS（CP932） | 'cp932'     | Excel で文字化けしないが使用可能な文字が限られる。                                         |

## JSON 形式
JSON（JavaScript Object Notation）。JavaScript の Object に由来する表記方法を使う Text format.
- list や dict を組み合わせた複雑な Data 構造を手軽に扱える。
- 明確な仕様が存在するため、実装による細やかな違いに悩くことがない。

# Python の Scraping 用 Library
## Beautiful Soup
- Simple かつわかりやすい API
- 内部の Parser を目的に応じて切り替えられる。
### Beautiful Soup で使用できる Parser
| Parser                   | 指定する Parser 名        | 特徴                      |
|--------------------------|----------------------|-------------------------|
| 標準 Library の html.parser | 'html.parser'        | 追加の Library が不要。        |
| lxml の HTML parser       | 'lxml'               | 高速に処理ができる。              |
| lxml の XML parser        | 'lxml-xml' または、'xml' | 唯一 XML に対応していて高速に処理できる。 |
| html5lib                 | 'html5lib'           | HTML5 の仕様通りに Parse できる。 |

## pyquery
- jQuery と同じような UI で Scrape できる
- 内部で lxml を使用している

# XML の Scraping
RSS など XML format が提供されている Web site は、HTML よりも簡単か確実に Parse できるので利用するとよい。  
<small>近年では Social media の台頭により RSS での提供は減少傾向にはある。</small>

XML からの Scraping は、CSS Selector より XPath の方が書きやすい Case が多い。

## RSS の Format の種類
RSS は、歴史的な経緯により複数の Format が混在している。
- RSS 1.0
- RSS 2.0
- Atom

RSS 2.0 が１番 Simple で解析しやすい。

# Database に保存する
単純に File に保存するのに比べて、複数 Process から読み書きしやすく、Data の重複を防ぎやすくなる。後の行程で分析に利用する際、条件に合う１部
の Data だけ取り出すのも簡単。

## Relational Database
- Relational Model, Transaction により Data の整合性を保つ。
- 標準化された SQL 文によって柔軟に Data を Query できる。

### SQLite
- 手軽に使える。
- File の書き込みに時間がかかる。少量の Data なら問題ないが、Crawl して取得した大量の Data を断続的に書き込むと、Bottle neck になりえる。
- ある Program が File に書き込んでいる間は、他の Program からは同じ File に書き込めないように Lock されるので、複数 Program からの同時
書き込みにも向いていない。

## NoSQL
- Relational Database 以外の Database の総称。
- 整合性を弱める代わりに Scalability や読み書きの性能が高い。
- Relational Database が向かない領域で広がっている。

### MongoDB
- NoSQL の一種。Document 型と呼ばれる Database。
- Open Software
- 柔軟な Data 構造と高い書き込み性能、使いやすさが特徴。
- １つの Database が複数の Collection を持ち、１つの Collection は複数の Document を持つ。
- Document は、BSON（JSON の Binary 版の形式）で扱われ、Python における list, dict のような複雑な Data 構造を格納できる。
- 事前に Data 構造を定義する必要がなく、Document 毎に異なる構造を持つことができるので Page によって掲載される Data 項目が異なる場合に役立つ。
- Relational Database に比べて Data の書き込み性能が高い。
 
# Crawler と URL
## Permalink
１つの Contents に対応し、時間が経っても対応する Contents が変わらない URL。

### Permalink を持つ Website
- 検索 Engin が Contents を認識しやすい。
- SNS に投稿しやすい。  
<small>※ 総じて SEO（検索 Engin 最適化）に強くなる。</small>

Permalink を利用する Web site には Link が一覧になっている Page が存在することが多い。  
  <small>※ 一覧 page と詳細 page の組み合わせで構成されている Pattern</small> 

**例外**
Ajax 実装で Link を Click したときに URL が変わらず Contents だけが変わる Siteは、一覧 Page のみの Pattern 、となる。

### 再実行を考慮した設計
- Crawl して取得した Data を Database に保存するときは、Data を一意に識別する Key について考える必要がある。
- 複数回、Crawl した時に取得した Contents が重複しないようにする。
- Data に一意の識別 Key を与え  
  - 新規 Data => 追加
  - 既存 Data => 最新の状態に更新

  となるようにする。

#### Key 候補
Crawl 対象の Web page が Contents を識別するために利用している id や Code 箇所などを URL から抽出するとよい。

### Database 設計
- 識別 Key を格納する Field に Unique 制約を設定して Data の一意正を担保する。
- Primary key は上記の識別 Key とは別に、Surrogate key と呼ばれる Unique な値を生成して使用するのがよい。 
  ※ URL から取得した値は、Web site 側の Renewal などで変更する可能性がある。

##### Surrogate key の例
- MySQL: AUTO_INCREMENT という属性で設定し、自動的な連番を振らせる。
- MongoDB: ObjectId と美呼ばれる 12 byte の一意な ID が _id という名前で自動的に設定される。
- uuid module で UUID を生成して使用する。

# 実用のためのノウハウ
## Crawler の特性
- 状態を持つ Crawler
- JavaScript を解釈する Crawler
- 不特定多数の Web site を対象とする Crawler

### 状態を持つ Crawler
Login が必要な Website を crawl するには Cookie に対応する Crawler

### JavaScript を解釈する Crawler
JavaScript で Contents の表示を行なっているような Website を Crawl するため Crawler  
Web browser を自動操作するための Tool が必要になる。  
HTML のみを解釈する Crawler に比べて１page あたりの処理に時間がかかり,Memory 消費が増える傾向。
JavaScript の実行が必要な Page に絞って使うなど工夫が必要。

#### Web browser を自動操作のための Tool
##### Selenium
Program から Browser を自動操作する Tool。Python からも利用するための Library も提供あり。
##### Puppeteer
Google Chrome を自動操作するための Node.js Library。  
Google Chrome しか対応していないが **Selenium** に比べて細やかな制御が可能。  
**Pyppeteer** という Library で Python で利用可能。

##### Chrome & Firefox の Headless mode 
GUI を使用しないで Browse を実行する Mode. Memory などの Resource 消費も少ない。

### 不特定多数の Web site を対象とする Crawler
- 特定の Web site だけを対象とする Crawler に比べて難易度が上がる。
- Page 内から１番主要と思われる文章や画像を取得するといった Page 構造に依存しない仕組みが必要とされることも多い。  
- Crawl 対象の Page も膨大になるので、同時平行処理による高速化が重要になる。
- 抽出した Data を Storage に保存する際の書き込み速度にも注意が必要。

## 取集した Data の利用に関する注意
### 4.2.1 著作権
特に Crawler の作成において注意が必要な３つの権利

| 権利    | 説明                              |
|-------|---------------------------------|
| 複製権   | 収集した Web page を保存する権利           |
| 翻案権   | 収集した Web page から新たな著作物を創造する権利   |
| 公衆送信権 | 収集した Web page を Server から公開する権利 |

上記、行為は基本的に著作権者の許諾が必要。しかし
- 私的使用の範囲内の複製など、使用目的によっては許諾不要。
- 情報解析を目的とした複製や検索 Engin service の提供を目的とした複製・翻案・自動公衆送信は2009年の著作権法改正により許諾不要になった。

事項のように細かい条件あり
- 会員のみが閲覧可能な Site の Crawl には著作権者の許諾が必要。
- robot.xtx や robot meta tag で拒否されている page は crawl しない。
- Crawl した後に拒否されたことがわかった場合は保存済みの著作物を消去する。
- 検索結果では元の Web page に link をする。
- 検索結果として表示する著作物は必要と認められる限度内。
- 違法 Contents であることを知った場合は公衆送信をやめる。

### 4.2.2 利用規約と個人情報
#### 利用規約
Web site で利用規約に crawling が明示的に禁止されている場合があるので確認が必要。

#### 個人情報
- たとえ Web site に公開されている情報でも個人情報を収集する場合は、基本的には利用目的を本人い通知し、利用の許諾を得る必要あり。
- EU 市民の個人情報を収集する場合は、2018年５月に施行された GDPR に従い取り扱わないと、非常に高額な制裁金を課される可能性あり。

## Crawl 先の負荷に関する注意
自身の Crawler が Web server の処理能力を多く占めると他者が Web site を閲覧できなくなってしまう。商用 Site の場合、営業妨害となる可能性もあるので
crawl 先に負荷をかけ過ぎないように配慮する。  
※ BAN されてしまうと継続的な Data 収集も困難になる。

- 適切な crawl 間隔を空ける
- robot.txt に従う
- 連絡先を明示する
- 適切な Error 処理を行なう

などを守る。

### 同時接続数と crawl 間隔
#### 同時接続数
Crawler の同時接続数は６よりも減らす。基本的には単一接続にするべき。

#### crawl 間隔
- 慣例として１秒以上の wait を入れる。
- robot.txt に Crawl-delay が存在する場合は、その秒数の間隔を空けて Request する

#### RSS や XML site map
HTML を取得する以外の手段が存在する場合は、なるべくその手段を用いる。
- HTML に比べて Server の負荷が少ない。
- Download する File size も小さい。

#### Cache の活用
一度 crawl した page は Cache し、一定の時間内は同じ page を crawl しないようにすることで負荷を軽減可能。

### robot.txt
| Directive   | 説明                                |
|-------------|-----------------------------------|
| User-agent  | 以降の Directive の対象となる Crawler を表す。 |
| Disallow    | crawl を禁止する pass を表す。             |
| Allow       | crawl を許可する pass を表す。             |
| Sitemap     | XML site map の URL を表す            |
| Crawl-delay | crawl 間隔を表す                       |

### robot meta tag
```html
<meta name="robots" content="noindex">
```

| content   | 説明                                    |
|-----------|---------------------------------------|
| nofollow  | この page 内の link をたどることを許可しない          |
| noarchive | この page を arcive として保存することを許可しない      |
| noindex   | この page を検索 Engine に index することを許可しない |

### Site map
XML site map は、Web site の管理者が Crawler に対して crawl して欲しい URL の List を提示するための XML file
参照すると効率的。

### 連絡先の明示
連絡先を明示する手段として Crawler が送信する HTTP request の User-Agent Header に連絡先の URL や Mail address を書く方法がある。

### Status code と Error 処理
余計な負荷をかけない行儀の良い Crawler を作るためには Error 処理も大切。
Web server が Access 過多という response を返しているのに何度も繰り返し request を送るといつまで経っても access 過多の状態が解消されない。

#### Error の種類
##### Network level の Error
DNS 解決の失敗や通信の timeout など、Server と正常に通信できない場合に発生。

##### HTTP level の Error
Web server は HTTP response の Status code で request の結果をかえす。
- 4xx: Client Error
- 5xx: Server Error

| Status code               | 説明                                                   |
|---------------------------|------------------------------------------------------|
| 100 Continue              | request が継続している。                                     |
| 200 OK                    | request は成功した。                                       |
| 301 Moved Permanently     | request した Resource は、恒久的に移動した。                      |
| 302 Found                 | request した Resource は一時的に移動した。                       |
| 304 Not Modified          | request した Resource は更新されていない。                       |
| 400 Bad Request           | Client の request に問題があるため処理できない。                     |
| 401 Unauthorized          | 認証されていないため処理できない。                                    |
| 403 Forbidden             | request は許可されていない。                                   |
| 404 Not Found             | request した Resource は存在しない。                          |
| 408 Request Timeout       | 一定時間内に request の送信を完了しなかった。                          |
| 500 Internal Server Error | Server 内部で予期せぬ Error が発生した。                          |
| 502 Bad Gateway           | Gateway server が背後の Server から Error を受け取った。          |
| 503 Service Unavailable   | Server は一時的に request を処理できない。                        |
| 504 Gateway Timeout       | Gateway server あら背後の Server への request が timeout した。 |

### HTTP 通信における Error 処理
Error が発生した時の対処法
- 時間をおいて Retry
- その page を諦める

#### 時間をおいて Retry
１時的な Error と考えられる場合は Retry。  
Retry が増えるたびに指数関数的に Retry間隔を増やすと Server の負荷を軽減できる。  

###### １自適な Error と考えられるもの
- Network level の Errorは、設定が間違っていなければ
- HTTP error のうち Status code が、408, 500, 502, 503, 504 のもの

#### Crawler 自体を停止する Case
単一 Page だけではなく同じ Site の 別 Page でも同じ Error が継続的に発生する場合。
