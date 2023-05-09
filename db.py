import sqlite3

#dette er koden som linker sql og nettsiden
conn = sqlite3.connect("database.db")
print("opened db with sucess")

conn.execute("CREATE TABLE login (username TEXT, pwd TEXT, number NUMERIC, epost TEXT)")
print("table created sucessfully")

conn.close()