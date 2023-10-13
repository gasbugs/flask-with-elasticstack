"""flaskrestx, elasticsearch 관련 라이브러리 임포트"""
import json

from elasticsearch import Elasticsearch
from flask import Flask, request
from flask_restx import Api, Resource

# Elasticsearch 인스턴스 생성
es = Elasticsearch(["https://127.0.0.1:9200"],
                   verify_certs=False,
                   basic_auth=('elastic', 'test1234'))

# Flask 애플리케이션 생성
app = Flask(__name__)
api = Api(app)


# API 정의
@api.route('/search')
class Search(Resource):
    """검색 기능"""
    @api.doc(description="책 검색")
    def get(self, title="", author="", category="", 
            written="", pages="", sell=""):
        """책 검색"""

        # 검색 조건을 가져옵니다.
        query = request.args
        search_query = {"query": {"bool": {"must": []}}}
        
        if title:
            append_query = {"match": {"title": {"query": title, "operator": "or"}}}
            search_query.append(append_query)
        if author:
            append_query = {"match": {"author": {"query": author, "operator": "or"}}}
            search_query.append(append_query)
        if category:
            append_query = {"match": {"category": {"query": category, "operator": "or"}}}
            search_query.append(append_query)
        if written:
            append_query = {"match": {"category": {"query": category, "operator": "or"}}}
            search_query.append(append_query)
        # 검색 질의를 생성합니다.
        search_query = {
            "query": {
                "bool": {
                    "must": [
                        ,
                        {
                            "match": {
                                "author": {
                                    "query": query.get("author"),
                                    "operator": "or",
                                }
                            }
                        },
                        {
                            "match": {
                                "category": {
                                    "query": query.get("category"),
                                    "operator": "or",
                                }
                            }
                        },
                        {
                            "range": {
                                "written": {
                                    "gte": query.get("written", {}).get("min"),
                                    "lte": query.get("written", {}).get("max"),
                                }
                            }
                        },
                        {
                            "range": {
                                "pages": {
                                    "gte": query.get("pages", {}).get("min"),
                                    "lte": query.get("pages", {}).get("max"),
                                }
                            }
                        },
                        {
                            "range": {
                                "sell": {
                                    "gte": query.get("sell", {}).get("min"),
                                    "lte": query.get("sell", {}).get("max"),
                                }
                            }
                        },
                    ]
                }
            }
        }

        # 검색을 수행합니다.
        response = es.search(index="books", query=search_query)

        # 검색 결과를 반환합니다.
        return json.dumps(response)


# API 실행
if __name__ == "__main__":
    app.run(debug=True)
