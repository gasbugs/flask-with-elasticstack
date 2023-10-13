"""flask를 임포트"""
from flask import Flask

app = Flask(__name__)


# endpoint 이름을 "hello-endpoint"로 변경(기본값: 함수 이름)
# methods를 사용하여 허가할 메서드 선택
@app.route("/hello", methods=["GET"], endpoint="hello-endpoint")
def hello():
    """/hello2에 요청이 들어오면 간단한 문자열로 리턴 수행"""
    return "Hello, Flask!"


if __name__ == "__main__":
    app.run()
