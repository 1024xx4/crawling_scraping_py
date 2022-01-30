import sys
from typing import List

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTContainer, LTTextBox, LTComponent
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage


def main():
    """
    Main となる処理。Command line 引数で指定した PDF File から、Textbox を抽出して中身を表示する。
    :return: Str
    """
    laparams = LAParams(detect_vertical=True)  # Layout Analysis の設定で縦書きの検出を有効にする。
    resource_manager = PDFResourceManager()  # 共有の Resorce を管理する Resorce Manager を作成。
    device = PDFPageAggregator(resource_manager, laparams=laparams)  # Page を集める PageAggregator Object を作成。
    interpreter = PDFPageInterpreter(resource_manager, device)  # Interpreter Object を作成。

    with open(sys.argv[1], 'rb') as f:  # File を Binary 形式で開く。
        # PDFPage.get_pages() に File Object を指定して、PDFPage Object を順に取得する。
        # 時間がかかる File は、Keyword 引数 pagenos で処理する Page 番号（０始まり）の List を指定するとよい。
        for page in PDFPage.get_pages(f):
            interpreter.process_page(page)  # page を処理する。
            layout = device.get_result()  # LTPage Object を取得。

            boxes = find_textboxes_recursively(layout)  # Page 内の Textbox の List を取得する。
            # Textbox の左上の座標の順で Textbox を sort する。
            # y1(Ｙ座標の値）は上に行くほど大きくなるので、正負を反転させている。
            boxes.sort(key=lambda b: (-b.y1, b.x0))

            for box in boxes:
                print('-' * 10)  # 読みやすいように区切り線を表示する。
                print(box.get_text().strip())  # Textbox 内の Text を表示する。


def find_textboxes_recursively(component: LTComponent) -> List[LTTextBox]:
    """
    再帰的に Textbox(LTTextBox)を探して、Textbox の List を取得する。
    :param component: LTComponent
    :return: List[LTTextBox]
    """
    # LTTextBox を継承する Object の場合は１要素の List を返す。
    if isinstance(component, LTTextBox):
        return [component]

    # LTContainer を継承する Objcet は子要素を含むので、再帰的に探す。
    if isinstance(component, LTContainer):
        boxes = []
        for child in component:
            boxes.extend((find_textboxes_recursively(child)))

        return boxes

    return []  # その他の場合は空の List を返す。


if __name__ == '__main__':
    main()
