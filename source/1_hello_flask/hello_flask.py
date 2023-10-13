"""flask 라이브러리 임포트"""
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    """인덱스 페이지 처리"""
    return 'Hello Flask!'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
