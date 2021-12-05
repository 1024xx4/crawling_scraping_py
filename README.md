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

