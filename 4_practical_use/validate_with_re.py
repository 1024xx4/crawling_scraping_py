import re


def validate_Price(value: str):
    """
    value が価格として正しい文字列（数字と Comma のみを含む文字列）であるかどうかを判別し、正しくない値の場合は例外 Value Error を発生させる。
    :param value: str
    :return: Value Error
    """
    if not re.search(r'^[0-9,]+$', value):  # 数字と Comma のみを含む正規表現に match するか check する。
        raise ValueError(f'Invalid price: {value}')  # match しない場合は例外を発生させる。


validate_Price('3,000')
validate_Price('無料')
