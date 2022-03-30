import hashlib
import json
import logging
import sys

from elasticsearch import Elasticsearch


def main():
    """
    Main となる処理
    """
    es = Elasticsearch(['localhost:9200'])
    create_page_index(es)

    for line in sys.stdin:
        page = json.loads(line)
        doc_id = hashlib.sha1(page['url'].encode('utf-8')).hexdigest()
        es.index(index='pages', doc_type='_doc', id=doc_id, body=page)


def create_page_index(es: Elasticsearch):
    """
    Elasticsearch に pages index を作成する
    """
    es.indices.create(index='pages', ignore=400, body={
        "settings": {
            "analysis": {
                "analyzer": {
                    "kuromoji_analyzer": {
                        "tokenizer": "kuromoji_tokenizer"
                    }
                }
            }
        },
        "mappings": {
            "_doc": {
                "properties": {
                    "url": {"type": "text"},
                    "title": {"type": "text", "analyzer": "kuromoji_analyzer"},
                    "content": {"type": "text", "analyzer": "kuromoji_analyzer"}
                }
            }
        }
    })


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
