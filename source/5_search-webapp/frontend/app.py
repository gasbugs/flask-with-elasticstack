import requests
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/search")
def show_loop():
    """루프를 구성할 데이터를 전달하여 렌더링한다."""
    args = dict(request.args)
    for arg in request.args:
        if not args[arg]:
            del args[arg]
    response = requests.get("http://127.0.0.1:5000/search",
                            params=args)
    results = response.json()
    print(results)
    results_list = results["hits"]["hits"]
    count_of_result = results["hits"]["total"]["value"]
    return render_template("search.html", results_list=results_list,
                           count_of_result=count_of_result)


# index 렌더링
@app.route("/")
def index():
    """index 파일을 참조할 수 있도록 렌더링한다."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
