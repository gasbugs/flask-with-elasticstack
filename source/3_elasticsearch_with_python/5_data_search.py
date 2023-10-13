"""엘라스틱서치 관련 라이브러리 임포트"""
from elasticsearch import Elasticsearch

es = Elasticsearch(["http://127.0.0.1:9200"])
data = es.search(index="my_index",
                 query={"match_all": {}})
print(data)
