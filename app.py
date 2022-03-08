from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from dbconnection import db
import mysql.connector
from flaskext.mysql import MySQL #pip install flask-mysql
import pymysql


connection = mysql.connector.connect(host="localhost", port="3306", database="bazasm", user="root", password="Savakiran03")
cursor = connection.cursor()

app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Savakiran03'
app.config['MYSQL_DATABASE_DB'] = 'bazasm'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


app.secret_key = "super secret key"

@app.route('/')
def index():  # put application's code here
    return render_template("index.html")

@app.route('/base')
def base():  # put application's code here
    return render_template("base.html", username = session["username"])

@app.route('/nw')
def nw():
    return render_template("index_nw.html")

@app.route('/ns')
def ns():
    return render_template("index_ns.html")

@app.route('/ce')
def ce():
    return render_template("index_ce.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        message = "Błędny login"
        username = request.form["username"]
        password = request.form["password"]
        cursor.execute("SELECT * FROM uzytkownicy WHERE username = %s AND password = %s", (username, password))
        record = cursor.fetchone()
        if record:
            session["loggedin"] = True
            session["username"] = record[1]
            return redirect(url_for("base"))
        else:
            return redirect(url_for('index'))

    return render_template("index.html")


@app.route("/logout")
def logout():
    session.pop("loggedin", None)
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/ajaxfile", methods=["POST", "GET"])
def ajaxfile():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if request.method == 'POST':
            draw = request.form['draw']
            row = int(request.form['start'])
            rowperpage = int(request.form['length'])
            searchValue = request.form["search[value]"]
            print(draw)
            print(row)
            print(rowperpage)
            print(searchValue)

            ## Total number of records without filtering
            cursor.execute("select count(*) as allcount from mieszkaniec")
            rsallcount = cursor.fetchone()
            totalRecords = rsallcount['allcount']
            print(totalRecords)

            ## Total number of records with filtering
            likeString = "%" + searchValue + "%"
            cursor.execute("SELECT count(*) as allcount from mieszkaniec WHERE indeks LIKE %s OR nazwaKarty LIKE %s OR adresKarty LIKE %s",
                (likeString, likeString, likeString))
            rsallcount = cursor.fetchone()
            totalRecordwithFilter = rsallcount['allcount']
            print(totalRecordwithFilter)

            ## Fetch records
            if searchValue == '':
                cursor.execute("SELECT * FROM mieszkaniec ORDER BY indeks asc limit %s, %s;", (row, rowperpage))
                mieszkanieclist = cursor.fetchall()
            else:
                cursor.execute(
                    "SELECT * FROM mieszkaniec WHERE indeks LIKE %s OR nazwaKarty LIKE %s OR adresKarty LIKE %s limit %s, %s;",
                    (likeString, likeString, likeString, row, rowperpage))
                mieszkanieclist = cursor.fetchall()

            data = []
            for row in mieszkanieclist:
                data.append({
                    'indeks': row['indeks'],
                    'nazwakarty': row['nazwaKarty'],
                    'adresKarty': row['adresKarty'],
                    'klatkaSchodowa': row['klatkaSchodowa'],
                    'telefon': row['telefon'],
                    'administracja': row['administracja'],
                })

            response = {
                'draw': draw,
                'iTotalRecords': totalRecords,
                'iTotalDisplayRecords': totalRecordwithFilter,
                'aaData': data,
            }
            return jsonify(response)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)

