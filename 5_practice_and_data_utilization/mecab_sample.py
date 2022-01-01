import MeCab

tagger = MeCab.Tagger()
tagger.parse('')  # .parseToNode()の不具合を回避するための Hack.

# .parseToNode()で最初の形態素を表す Node object を取得する。
node = tagger.parseToNode('すもももももももものうち')

while node:
    # .surface は形態素の文字列、.feature は品詞などを含む文字列をそれぞれ表す。
    print(node.surface, node.feature)
    node = node.next  # .next で次の Node を取得する。
