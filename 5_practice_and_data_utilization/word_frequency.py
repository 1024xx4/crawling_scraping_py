import sys
import logging
from collections import Counter
from pathlib import Path
from typing import List, Iterator, TextIO  # TextIO は str を取得できる File Object を表す型。

import MeCab

tagger = MeCab.Tagger('')
tagger.parse('')  # これは.parseToNode()の不具合を回避するための Hack.


def main():
    """
    Commandline 引数で指定した Directory 内の File を読み込んで、頻出単語を表示する。
    :return: str, int
    """

    # Commandline の第１引数で、WikiExtractor の出力先の Directory を指定する。
    # Path object は File や Directory の Path 操作を抽象化する Object.
    input_dir = Path(sys.argv[1])

    # 単語の出現回数を格納する Counter object を作成する。
    # Counter class は、dict を継承しており、値として key の出現回数を保持する。
    frequency = Counter()

    # .glob()で Wildcard に match する File の List を取得し、match したすべての File を処理する。
    for path in sorted(input_dir.glob('*/wiki_*')):
        logging.info(f'Processing {path}...')

        with open(path) as file:  # File を開く。
            # File に含まれる記事内の単語の出現回数を数え、出現回数を merge する。
            frequency += count_words(file)

    # 全記事の処理が完了したら、上位30件の名詞と出現回数を表示する。
    for word, count in frequency.most_common(30):
        print(word, count)


def count_words(file: TextIO) -> Counter:
    """
    WikiExtractor が出力した File に含まれるすべての記事から単語の出現回数を数える関数
    :param file: TextIO
    :return: Counter
    """

    frequency = Counter()  # File 内の単語の出現頻度を数える Counter object.
    num_docs = 0  # Log 出力用に、処理した記事数を数えるための変数。

    for content in iter_doc_contents(file):  # File 内の全記事について反復処理する。
        words = get_words(content)  # 記事に含まれる名詞の List を取得する。
        # Counter の update() method に List などの反復可能 Object を指定すると、List に含まれる値の出現回数を一度に増やせる。
        frequency.update(words)
        num_docs += 1

    logging.info(f'Found {len(frequency)} words from {num_docs} documents.')
    return frequency


def iter_doc_contents(file: TextIO) -> Iterator[str]:
    """
    File object を読み込んで、記事の中身（開始 Tag <doc...> と終了 Tag </doc> の間の Text ）を順に繰り返す Generator 関数。
    :param file: TextIO
    :return: Iterator[str]
    """

    for line in file:  # File に含まれるすべての行について反復処理する。
        if line.startswith('<doc '):
            buffer = []  # 開始 Tag が見つかったら Buffer を初期化する。
        elif line.startswith('</doc>'):
            # 終了 Tag が見つかったら Buffer の中身を結合して yield する。
            content = ''.join(buffer)
            yield content
        else:
            buffer.append(line)  # 開始 Tag・終了 Tag 以外の行は Buffer に追加する。


def get_words(content: str) -> List[str]:
    """
    文字列内に出現する名詞の List（重複含む）を取得する関数。
    :param content: str
    :return: List[str]
    """

    words = []  # 出現する名詞を格納する List.

    node = tagger.parseToNode(content)
    while node:
        # node.feature は Comma で区切られた文字列なので、split() で分割して最初の２項目を pos と pos_sub1 に代入する。
        # pos は Part of Speech（品詞）の略。
        pos, pos_sub1 = node.feature.split(',')[:2]
        # 固有名詞または一般名詞の場合のみ words に追加する。
        if pos == '名詞' and pos_sub1 in ('固有名詞', '一般'):
            words.append(node.surface)
        node = node.next

    return words


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # INFO level 異常の Log を出力する。
    main()
