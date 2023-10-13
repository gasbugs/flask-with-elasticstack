from flask import Flask, url_for

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello Page!"


@app.route('/profile/<username>/')
def get_profile(username):
    return 'profile : ' + username


# 룰에 변수 지정하기
@app.route("/hello/<string:name>", methods=["GET"])
def hello_name(name):
    """/hello에 요청이 들어오면 간단한 문자열로 리턴 수행"""
    return f"Hello, {name}!"


if __name__ == "__main__":
    with app.test_request_context():
        print(url_for('get_profile', username='flask'))
    app.run()
