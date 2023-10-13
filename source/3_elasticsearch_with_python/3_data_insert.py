"""엘라스틱서치 관련 라이브러리 임포트"""
from elasticsearch import Elasticsearch

es = Elasticsearch(["http://127.0.0.1:9200"])

doc = {
        "name": "Choi",
        "Job": "IT security"
}

data = es.index(index="my_index", id="1", document=doc)
print(data)

# 문서 업데이트
document = {"name": "Jane Doe"}
data = es.update(index="my_index", id="1", doc=doc)
print(data)

# 문서 삭제
data = es.delete(index="my_index", id="1")
print(data)
