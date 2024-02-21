# flaskモジュールからFlaskクラスをインポート
from flask import Flask
# Flaskクラスをインスタンス化してapp変数に代入
app=Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!!"

@app.route("/<name>")
def name(name):
    return name+"さんこんにちは"

# スクリプトとして直接実行した場合
if __name__=="__main__":
    # FlaskのWEBアプリケーションを起動
    app.run(debug=True)