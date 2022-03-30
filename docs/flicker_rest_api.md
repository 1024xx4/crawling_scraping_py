# Flickr の API の使用

- API key を取得し curl で URL を呼び出すと XML形式の結果が得られる。

```shell
curl 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=*****&text=sushi&sort=relevance&license=4,5,6,9'
```
\****部分には Flickr の API key を入力

## Rest API
一番、Simple

### End point
```shell
https://api.flickr.com/services/rest/
```

### URL の Query Parameters
#### method(必須)
呼び出す API の Method名。`flicker.photos.search` は、指定した条件で写真を検索する。

#### api_key(必須)
あらかじめ取得しておいた Flickr の API key.

#### text(Optional)
検索語句。Flickr は海外の User が多いため、一般的に日本語よりも英語の検索語句のほうが多くの検索結果を得られる。

#### sort(Optional)
結果を Sort する順序。

#### license(Optional)
Comma で区切った License ID の List.
指定できる License ID の値は `flickr.photos.licenses.getInfo` method で取得できる。  
参照: https://www.flickr.com/services/api/flickr.photos.licenses.getInfo.html

#### その他、様々な Query Parameters
参照: https://www.flickr.com/services/api/flickr.photos.search.html

### Response される XML の構成
rsp 要素の中に photo 要素、その中に個々の写真を表す photo 要素がある。
```shell
<photo id="6817128733" owner="64436403@N04" secret="6251658b2f" server="7020" farm="8" title="DSC06754" ispublic="1" isfriend="0" isfamily="0" />
```
各属性を下記、Format に当てはめると、画像の URL を生成できる
```shell
https://farm{farm}.staticflickr.com/{server}/{id}_{secret}_{size}.jpg
```
{size} は Alphabet 文字で値を設定できる。

| Alphabet | 概要       | Size      |
|----------|----------|-----------|
| t        | Thumnail | 長辺: 100px |
| n        | 小        | 長辺 320px  |
| z        | 中        | 長辺 640px  |
| b        | 大        | 長辺 1024px |

参照: https://www.flickr.com/services/api/misc.urls.html

