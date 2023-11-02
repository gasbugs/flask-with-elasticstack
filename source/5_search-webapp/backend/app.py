"""flaskrestx, elasticsearch 관련 라이브러리 임포트"""
import json

from elasticsearch import Elasticsearch
from flask import Flask, request
from flask_restx import Api, Resource
from flask_restx import reqparse


# Elasticsearch 인스턴스 생성
es = Elasticsearch(["https://127.0.0.1:9200"],
                   verify_certs=False,
                   basic_auth=('elastic', 'test1234'))

# Flask 애플리케이션 생성
app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument("title", type=str)
parser.add_argument("author", type=str)
parser.add_argument("category", type=str)
parser.add_argument("written", type=str)
parser.add_argument("pages_min", type=int)
parser.add_argument("pages_max", type=int)
parser.add_argument("sell_min", type=int)
parser.add_argument("sell_max", type=int)


# API 정의
# http://127.0.0.1:443/search?title=The%20Tempest&category=Comedies&author=William%20Shakespeare&written=1600-01-01&pages_min=0&pages_max=100&sell_min=0&sell_max=300000000
@api.route('/search')
class Search(Resource):
    """검색 기능"""
    @api.expect(parser)
    def get(self):
        args = parser.parse_args()
        # print(args)

        """책 검색"""
        # 검색 조건을 가져옵니다.
        
        conditions = []

        for var in args.keys():
            if args[var] == None:
                continue
            if var in ['title', 'author', 'category']:
                append_query = {"match": {var: {"query": args[var]}}}
                conditions.append(append_query)

            elif var in ['pages_min']:
                append_query = {"range": {'pages': {"gte": args[var]}}}
                conditions.append(append_query)
            elif var in ['sell_min']:
                append_query = {"range": {'sell': {"gte": args[var]}}}
                conditions.append(append_query)
            
            elif var in ['pages_max']:
                append_query = {"range": {'pages': {"lte": args[var]}}}
                conditions.append(append_query)
            elif var in ['sell_max']:
                append_query = {"range": {'sell': {"lte": args[var]}}}
                conditions.append(append_query)
            
            elif var in ['written']:
                    append_query = {"range": {var: {"gte": args[var]}}}
                    conditions.append(append_query)

        search_query = {"bool": {"must": conditions}}

        print('search_query:', search_query)

        # 검색을 수행합니다.
        results = es.search(index="books", query=search_query)

        #print("result:", type(results), results)

        # 검색 결과를 반환합니다.
        return dict(results)


# API 실행
if __name__ == "__main__":
    app.run(debug=True)
