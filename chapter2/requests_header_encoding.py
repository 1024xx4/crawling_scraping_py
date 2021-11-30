import sys
import requests

url = sys.argv[1] # 第１引数から URL を取得する。
r = requests.get(url) # URL で指定した Web page を取得する。
print(f'encoding: {r.encoding}', file=sys.stderr) # Encoding を標準 Error 出力に出力する。
print(r.text) # Decode いｓた Response body を標準出力に出力する