"""flask로 부터 Flask 함수를 가져옴"""
from flask import Flask, redirect, request

app = Flask(__name__)


@app.before_request
def before_request():
    """http로 접근 시 https로 리다이렉션"""
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


@app.route('/hello')
def index():
    """hell world"""
    return "hello, world"


if __name__ == "__main__":
    # app.debug = True
    # context = ('cert.pem', 'key.pem')
    # app.run(host="0.0.0.0", port=443, ssl_context=context)
    # app.run(host="0.0.0.0", port=443, ssl_context='adhoc')
    app.run()
