"""엘라스틱서치 관련 라이브러리 임포트"""
from elasticsearch import Elasticsearch

es = Elasticsearch(["https://127.0.0.1:9200"],
                   verify_certs=False,
                   basic_auth=('elastic', 'test1234'))
# es = Elasticsearch(hosts="127.0.0.1", port=9200)
