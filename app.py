from flask import Flask, render_template, request
import sqlite3 as sql
#dette er flask koden her finner du meste parten av koden til nettsiden
app = Flask(__name__)
#dette er koden som lager en linken til hver side 
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/aboutus')
def aboutinfo():
    return render_template('aboutus.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signein')
def new_student():
    return render_template('signein.html')
#dette er koden sheker hva du skrev i sign in og putter det inn i databasen 
@app.route('/addrec', methods=['POST','GET'])
def addrec():
    if request.method == 'POST':
        try:
            username=request.form['username']
            pwd=request.form['pwd']
            number=request.form["number"]
            epost=request.form["epost"]

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO login (username, pwd, number, epost) VALUES (?,?,?,?)",(username,pwd,number,epost))
                con.commit()
                msg = "Record sucessfully added"
        except Exception as e:
            con.rollback()
            msg="error in insert operation" + str(e)
        finally:
            con.close()
            return render_template("result.html", msg=msg)

#dette er koden som sheker login informashonen din og gir deg riktig svar and på hva du skriver
@app.route('/testrec', methods=['POST'])
def testrec():
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
        con.close()
        if (len(records) >= 1):
            msg = "login sucsefull" + " " + str(username)
            return render_template("loginres.html", msg=msg)
        else:
            msg = "wrong loging informayshoi"
            return render_template("login.html", msg=msg)
            

#dette er koden som tar informashon fra databasen og sender den til tabelen i lite.html
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

