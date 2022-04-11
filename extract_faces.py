import logging
import sys
from pathlib import Path
from typing import Iterator

import cv2
from numpy import array


def main():
    """
    メインとなる処理
    """
    output_dir = Path('faces')
    output_dir.mkdir(exist_ok=True)
    classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
    for image_path in sys.argv[1:]:
        process_image(classifier, Path(image_path), output_dir)


def process_image(classifier: cv2.CascadeClassifier, image_path: Path, output_dir: Path):
    """
    １つの画像File を処理する。画像から抽出した顔画像を File に保存する。
    """
    logging.info(f'Processing {image_path}...')
    image = cv2.imread(str(image_path))

    if image is None:
        logging.info(f'Processing "{image_path}" not found.')
        exit(1)
        face_images = extract_faces(classifier, image)  # 顔を抽出する

        for i, face_image in enumerate(face_images):
            output_path = output_dir.joinpath(f'{image_path.stem}_{i}.jpg')
            cv2.imwrite(str(output_path), face_image)


def extract_faces(classifier: cv2.CascadeClassifier, image: array) -> Iterator[array]:
    """
    画像から顔を検出して、顔の部分を切り取った画像を yield する
    """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = classifier.detectMultiScale(gray_image)
    for x, y, w, h in faces:
        yield image[y:y + h, x:x + w]


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
