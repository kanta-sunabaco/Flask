# flaskモジュールからFlaskクラスをインポート
from flask import Flask,render_template
# Flaskクラスをインスタンス化してapp変数に代入
app=Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!!"

@app.route("/<name>")
def name(name):
    return name+"さんこんにちは"

@app.route("/template")
def template():
    py_name="すなばこ"
    return render_template("index.html",name=py_name)

# テストルーティング
@app.route("/test")
def test():
    py_name="すなばこ"
    return render_template("base.html",name=py_name)



# スクリプトとして直接実行した場合
if __name__=="__main__":
    # FlaskのWEBアプリケーションを起動
    app.run(debug=True)