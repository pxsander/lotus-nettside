from flask import Flask, render_template, url_for, request
import sqlite3 as sql

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enternew')
def new_student():
    return render_template('student.html')

@app.route('/login')
def new_login():
    return render_template('login.html')


@app.route('/addrec', methods=['POST','GET'])
def addrec():
    if request.method == 'POST':
        try:
            username=request.form['username']
            pwd=request.form['pwd']

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (username, pwd) VALUES (?,?)",(username,pwd))
                con.commit()
                msg = "Record sucessfully added"
        except:
            con.rollback()
            msg="error in insert operation"
        finally:
            return render_template("result.html", msg=msg)
            con.close()

@app.route('/testrec', methods=['POST','GET'])
def testrec():
    if request.method == 'POST':
        try:
            username=request.form['username']
            pwd=request.form['pwd']

            with sql.connect("database.db") as con:
                cur = con.cursor()
            
                sqlite_insert_query = """select * from login where username='""" + username + """' and pwd='""" + pwd + """'"""
                cur.execute(sqlite_insert_query)
                records = cur.fetchall()
        except:
            msg="wrong loging informayshoin"
        finally:
            if (len(records) >= 1):
                msg = "login sucsefull" + " " + str(records)
                return render_template("login2.html", msg=msg)
            else:
                msg = "wrong loging informayshoi"
                return render_template("index.html", msg=msg)
            con.close()

@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from login")
    rows = cur.fetchall()
    return render_template('list.html',rows=rows)

if __name__ == "__main__":
    app.run(debug=True)

