from flask import Flask, render_template

app = Flask(__name__)


# 템플릿 렌더링
@app.route("/name/<string:name>")
def show_name(name):
    """전달 받은 이름을 템플릿으로 출력한다."""
    return render_template("index.html", name=name)


@app.route("/loop/<string:name>")
def show_loop(name):
    """루프를 구성할 데이터를 전달하여 렌더링한다."""
    movies = [
        {'name': '타이타닉', 'year': 1998},
        {'name': '터미네이터', 'year': 1984}
    ]
    return render_template("loop.html", name=name, movies=movies)


# css 렌더링
@app.route("/css")
def show_css():
    """css 파일을 참조할 수 있도록 렌더링한다."""
    return render_template("css.html")


if __name__ == "__main__":
    app.run()
