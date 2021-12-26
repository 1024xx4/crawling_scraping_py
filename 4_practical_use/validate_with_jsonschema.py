from jsonschema import validate

# 次の４つの Rule を持つ Schema（期待する Data 構造）を定義する。
schema = {
    'type': 'object',  # Rule_1: 値は JSON における Object（Python における dict）である。
    'properties': {
        # Rule_2: name の値は文字列である。
        'name': {
            'type': 'string'
        },
        # Rule_3: price の値は文字列で、Pattern に指定した正規表現に match する。
        'price': {
            'type': 'string',
            'pattern': '^[0-9,]+$'
        }
    },
    'required': ['name', 'price']  # Rule_4: dict の Key として name と price は必須である。
}

# validate()関数は、第１引数の Object を第２引数の Schema で Validation する。
validate({
    'name': 'ぶどう',
    'price': '3,000',
}, schema) # Schema に適合するので例外は発生しない。

validate({
    'name': 'みかん',
    'price': '無料',
}, schema) # Schema に適合しないので、例外 jsonschema.exceptions.ValidationError が発生する。

