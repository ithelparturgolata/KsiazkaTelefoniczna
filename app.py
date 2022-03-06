from flask import Flask, render_template, request, redirect, url_for, session
from dbconnection import db
import mysql.connector

connection = mysql.connector.connect(host="localhost", port="3306", database="bazasm", user="root", password="Savakiran03")
cursor = connection.cursor()

app = Flask(__name__)

app.secret_key = "super secret key"

@app.route('/')
def index():  # put application's code here
    return render_template("index.html")

@app.route('/menu')
def menu():  # put application's code here
    return render_template("menu.html")

@app.route('/base')
def base():  # put application's code here
    return render_template("base.html", username = session["username"])

@app.route('/nw')
def nw():  # put application's code here
    cursor.execute("SELECT * FROM mieszkaniec WHERE administracja='NW'")
    admin_nw = cursor.fetchall()
    return render_template("nw.html", admin = admin_nw)

@app.route('/ns')
def ns():  # put application's code here
    cursor.execute("SELECT * FROM mieszkaniec WHERE administracja='NS'")
    admin_ns = cursor.fetchall()
    return render_template("ns.html", admin = admin_ns)

@app.route('/ce')
def ce():  # put application's code here
    cursor.execute("SELECT * FROM mieszkaniec WHERE administracja='CE'")
    admin_ce = cursor.fetchall()
    return render_template("ce.html", admin = admin_ce)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        message = ""
        username = request.form["username"]
        password = request.form["password"]
        cursor.execute("SELECT * FROM uzytkownicy WHERE username = %s AND password = %s", (username, password))
        record = cursor.fetchone()
        if record:
            session["loggedin"] = True
            session["username"] = record[1]
            return redirect(url_for("base"))
        else:
            message = "Podałeś błędny login lub hasło"

    return render_template("index.html")

@app.route("/logout")
def logout():
    session.pop("loggedin", None)
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)

