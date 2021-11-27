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
Option | 説明
--- | ---
-V, -version | Wget の Version を表示する。
-h, --help | Help を表示する。
-q, --quit | 進捗状況などを表示しない。
-O *file*, --output-document=*file* | *file* に保存する。
-c, --continue | 前回の続きから File の Download を再開する。
-r, --recursive | Link をたどって再帰的に Download する。
-l *depth*, --level=*depth* | 再帰的に Download するときに Link をたどる深さを *depth* に制限する。
-w *seconds*, --wait=*seconds* | 再帰的に Download するときに Download 感覚として *seconds* 秒空ける。
-np, --no-parent | 再帰的に Download するときに親 Directory を Crawl しない。
-l *list*, --include *list* | 再帰的に Download するときに *list*に含まれる Directory のみをたどる。
-N, --timestamping | File が更新されているときのみ Download する。
-m, --mirror | Mirroring 用の Option を有効化する。
--restrict-file-names=nocontrol | URL に日本語が含まれる場合に、日本語の File 名で保存する。
