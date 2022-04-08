import logging
import sys

import cv2

logging.basicConfig(level=logging.INFO)  # INFO Level 以上の Log を出力する。

try:
    input_path = sys.argv[1]  # 第１引数は入力画像の Path
    output_path = sys.argv[2]  # 第２引数は出力画像の Path
except IndexError:
    # Command line 引数が足りない場合は使い方を表示して終了する。
    print('Usage: python detect_faces.py INPUT_PATH OUTPUT_PATH', file=sys.stderr)
    exit(1)

# 特徴量File の Path を指定して、分類機Object を作成する。
# ここでは OpenCV に付属している学習済みの顔の特徴量File を使用する。
# cv2.data.haarcascades は、Data directory の Path. 公式の Python binding には存在しないので注意。
classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')

image = cv2.imread(input_path)  # 画像File を読み込む
if image is None:
    # 画像File が存在しない場合は Error を表示して終了する。
    logging.error(f'Image "{input_path}" not found.')
    exit(1)

# 顔を出力する。特徴量File が存在しない場合はこの時点で Error になるので注意。
faces = classifier.detectMultiScale(image)
logging.info(f'Found {len(faces)} faces.')  # 検出できた顔の数を出力。

# 検出された顔の List について反復処理し、顔を囲む白い四角形を描画する。
# x, y, w, h はそれぞれ検出された顔のＸ座標、Ｙ座標、幅、高さを表す。
for x, y, w, h in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), color=(255, 255, 255), thickness=2)

cv2.imwrite(output_path, image)  # 四角形を描画した結果の画像を保存する。
