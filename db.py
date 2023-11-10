import sqlite3 as sql

# Makes the main connection
con = sql.connect("main.db")
print("hi")

def check():
    # Checks for tables
    cur = con.cursor()
    command = """CREATE TABLE IF NOT EXISTS customers (
        name TEXT)"""

    cur.execute(command)
    cur.close()
    con.commit()

def add(name):
    cur = con.cursor()
    command = """INSERT INTO customers(name) VALUES(?)"""

    cur.execute(command, (name,))

    con.commit()


