#%%
from flask import Flask, render_template, request
import sqlite3 as sql
import pandas as pd
#dette er flask koden her finner du meste parten av koden til nettsiden
app = Flask(__name__)
#dette er koden som lager en linken til hver side 
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/aboutus')
def aboutinfo():
    return render_template('aboutus.html')

@app.route('/pwdup')
def pwdup():
    return render_template('pwdup.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signin')
def new_student():
    return render_template('signin.html')

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

#dette er koden som tilater deg og gi app.py en xlsx file og der etter putte en liste med nye bruke og putte det in i databasen med bruker navn passord og email
@app.cli.command("autoaddrec")        
def autoaddrec():
    users= pd.read_excel("users.xlsx",header=None)
    colum=users[0].to_list()
    print (users)
    for text in colum:
        print (text)
        domene = "lotus.com"
        _,name=text.split(" ", 1)
        førstenavne,eternavne=name.split(" ", 1)
        username = førstenavne[:4].lower() + eternavne[:3].lower()
        epost = username + "@" + domene
        pwd = "lotus"
        number = "no phone number"
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO login (username, pwd, number, epost) VALUES (?,?,?,?)",(username,pwd,number,epost))
            con.commit()

#dette er koden som sheker login informashonen din og gir deg riktig svar and på hva du skriver
@app.route('/testrec', methods=['POST'])
def testrec():
    try:
        username = request.form['username']
        pwd = request.form['pwd']
        with sql.connect("database.db") as con:
            cur = con.cursor()
            sqlite_insert_query = "SELECT * FROM login WHERE username=? AND pwd=?"
            cur.execute(sqlite_insert_query, (username, pwd))
            records = cur.fetchall()
    except:
        msg = "Feil påloggingsinformasjon"
    finally:
        con.close()
        if len(records) >= 1:
            if username == "admin":
                msg = "Administrator pålogget: " + str(username)
                return render_template("admin.html", msg=msg)
            elif pwd == "lotus":
                msg = "første gang du loger på trenger du å oppdatere passorde"
                return render_template("pwdup.html", msg=msg)
            else:
                msg = "Pålogging vellykket: " + str(username)
                return render_template("loginres.html", msg=msg)
        else:
            msg = "Feil påloggingsinformasjon"
            return render_template("login.html", msg=msg)

#dette er koden som sheker og oppdaterer passorde
@app.route('/updaterec', methods=['POST','GET'])
def updaterec():
    try:
        username = request.form['username']
        pwd = request.form['pwd']
        newpwd = request.form["newpwd"]
        with sql.connect("database.db") as con:
            cur = con.cursor()            
            sqlite_insert_query = "SELECT * FROM login WHERE username=? AND pwd=?"
            cur.execute(sqlite_insert_query, (username, pwd))
            records = cur.fetchall()
            if len(records) >= 1:
                updatequery = "UPDATE login set pwd=? where username=?"
                cur.execute(updatequery, (newpwd, username))
    except:
        msg = "Feil informasjon"
    finally:
        con.close()
        if len(records) >= 1:
            msg = "Pålogging vellykket: " + str(username)
            return render_template("loginres.html", msg=msg)
        else:
            msg = "Feil informasjon"
            return render_template("pwdup.html", msg=msg)

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
    
# %%
