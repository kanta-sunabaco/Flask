# flaskモジュールからFlaskクラスをインポート
from flask import Flask,render_template,request,redirect,session
import sqlite3
# Flaskクラスをインスタンス化してapp変数に代入
app=Flask(__name__)

# secret_keyでセッション情報を暗号化
app.secret_key="SUNABACO2024"

@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/list")
    else:
        return render_template("index.html")


# タスク追加ページ
@app.route("/add")
def add_get():
    if "user_id" in session:
        return render_template("add.html")
    else:
        return redirect("/")

@app.route("/add",methods=["POST"])
def add_post():
    if "user_id" in session:
        user_id=session["user_id"][0]
        # 1.入力フォームからデータを取得する
        task=request.form.get("task")
        print(task)
        # 2.データベースに接続する
        con=sqlite3.connect("myTask.db")
        # 3.データベースを操作するための準備
        c=con.cursor()
        # 4.SQLを実行してDBにデータを送る
        c.execute("INSERT INTO tasks (id,task,user_id) VALUES (null,?,?)",(task,user_id))
        # 5.データベースを更新（保存）する
        con.commit()
        # 6.データベースの接続を終了する
        c.close()
        return redirect("/list")
    else:
        redirect("/")

@app.route("/list")
def list_get():
    if "user_id" in session:
        user_id=session["user_id"][0]
        con=sqlite3.connect("myTask.db")
        # 3.データベースを操作するための準備
        c=con.cursor()
        c.execute("SELECT name FROM users WHERE id=?",(user_id,))
        user_name=c.fetchone()[0]
        # 4.SQLを実行してDBにデータを送る
        c.execute("SELECT id,task FROM tasks WHERE user_id=?;",(user_id,))
        # 6.データベースの接続を終了する
        task_list=[]
        for row in c.fetchall():
            print(row)
            task_list.append({"id":row[0],"task":row[1]})
            print(task_list)
        c.close()
        return render_template("list.html",task_list=task_list,user_name=user_name)
    else:
        return redirect("/")

@app.route("/edit/<int:task_id>")
def edit_get(task_id):
    if "user_id" in session:
        con=sqlite3.connect("myTask.db")
        c=con.cursor()
        c.execute("SELECT task FROM tasks WHERE id=?;",(task_id,))
        task=c.fetchone()
        task=task[0]
        c.close()
        return render_template("edit.html",task=task,task_id=task_id)
    else:
        return redirect("/")

@app.route("/edit",methods=["POST"])
def edit_post():
    if "user_id" in session:
        task=request.form.get("task")
        task_id=request.form.get("task_id")
        con=sqlite3.connect("myTask.db")
        c=con.cursor()
        c.execute("UPDATE tasks SET task=? WHERE id=?;",(task,task_id))
        con.commit()
        c.close()
        return redirect("/list")
    else:
        return redirect("/")

# 削除機能
@app.route("/delete/<int:task_id>")
def delete(task_id):
    if "user_id" in session:
        con=sqlite3.connect("myTask.db")
        c=con.cursor()
        c.execute("DELETE FROM tasks WHERE id=?;",(task_id,))
        con.commit()
        c.close()
        return redirect("/list")
    else:
        return redirect("/")


# 新規登録機能
@app.route("/regist")
def regist_get():
    if "user_id" in session:
        return redirect("/list")
    else:
        return render_template("regist.html")

@app.route("/regist",methods=["POST"])
def regist_post():
    name=request.form.get("name")
    password=request.form.get("password")
    con=sqlite3.connect("myTask.db")
    c=con.cursor()
    c.execute("INSERT INTO users (id,name,pass) VALUES (null,?,?)",(name,password))
    con.commit()
    c.close()
    return redirect("/login")

# ログイン
@app.route("/login")
def login_get():
    if "user_id" in session:
        return redirect("/list")
    else:
        return render_template("login.html")

# ログイン処理
@app.route("/login",methods=["POST"])
def login_post():
    name=request.form.get("name")
    password=request.form.get("password")
    con=sqlite3.connect("myTask.db")
    c=con.cursor()
    c.execute("SELECT id FROM users WHERE name=? and pass=?;",(name,password))
    id=c.fetchone()
    c.close()
    if id is None:
        return redirect("/login")
    else:
        session["user_id"]=id
        return redirect("/list")

# ログアウト
@app.route("/logout")
def logout():
    session.pop("user_id",None)
    return redirect("/")

@app.errorhandler(404)
def page_not_found(error):
    return "ページが見つかりません！", 404
    # return render_template('page_not_found.html'), 404


# スクリプトとして直接実行した場合
if __name__=="__main__":
    # FlaskのWEBアプリケーションを起動
    app.run(debug=True)