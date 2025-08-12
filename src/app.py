from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

db = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "Destemido_007",
    database ="login_screen"

)

@app.route("/", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

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
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(sql, (username, password))
        db.commit()
        
        return redirect("/")
    
    return render_template("register.html")


@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

if __name__== "__main__":
    app.run(debug=True)