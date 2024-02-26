# flaskモジュールからFlaskクラスをインポート
from flask import Flask,render_template,request

import sqlite3
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

# タスク追加ページ
@app.route("/add")
def add_get():
    return render_template("add.html")


@app.route("/add",methods=["POST"])
def add_post():
    # 1.入力フォームからデータを取得する
    task=request.form.get("task")
    print(task)
    # 2.データベースに接続する
    con=sqlite3.connect("myTask.db")
    # 3.データベースを操作するための準備
    c=con.cursor()
    # 4.SQLを実行してDBにデータを送る
    c.execute("INSERT INTO tasks (id,task) VALUES (null,?)",(task,))
    # 5.データベースを更新（保存）する
    con.commit()
    # 6.データベースの接続を終了する
    c.close()
    return render_template("add.html")






# スクリプトとして直接実行した場合
if __name__=="__main__":
    # FlaskのWEBアプリケーションを起動
    app.run(debug=True)