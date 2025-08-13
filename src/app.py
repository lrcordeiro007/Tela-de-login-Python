from flask import Flask, render_template, request, redirect, url_for , session
import pymysql 
import os

app = Flask(__name__)
app.secret_key = 'uma_chave_secreta_qualquer'

db = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "Destemido_007",
    database ="login_screen"

)
@app.route("/")
def start():
    return render_template("start.html")


@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        cursor = db.cursor()
        sql = "SELECT id FROM users WHERE username= %s"
        cursor.execute(sql, (username))
        user = cursor.fetchone()

        if user:
            session['user_id']= user[0]
        else :
            return "Usuário não encontrado", 404

        cursor = db.cursor()
        sql = "SELECT username FROM users WHERE password=%s"
        cursor.execute(sql, (password))
        result = cursor.fetchone()
      

        if result:
            return redirect (url_for("welcome"))
        else:
            return render_template("login.html",
            error="Invalid username or password")

    return render_template("login.html")

@app.route("/register",methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        cursor = db.cursor()
        sql_user = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(sql_user, (username, password))
        db.commit()
        
        return redirect("/")
    
    return render_template("register.html")


@app.route("/welcome", methods = ["GET", "POST"])
def welcome():
    if request.method == "POST":
        post = request.form.get("post")
        user_id = session['user_id']

        cursor = db.cursor()
        sql_post = "INSERT INTO post (post, user_id) VALUES (%s, %s)" 
        cursor.execute(sql_post, (post, user_id))
        db.commit()
        
        return redirect ("/welcome")
    return render_template("welcome.html")
 


if __name__== "__main__":
    app.run(debug=True)