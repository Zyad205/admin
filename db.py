import sqlite3 as sql

# Makes the main connection
con = sql.connect("main.db")

def check() -> None:
    # Checks for tables
    cur = con.cursor()

    command = """CREATE TABLE IF NOT EXISTS customers (
        name TEXT PRIMARY KEY,
        last_sub TEXT,
        next_sub TEXT)"""

    cur.execute(command)
    cur.close()

    con.commit()

def add(name: str, last_sub: str, next_sub: str) -> None:
    cur = con.cursor()
    command = """INSERT INTO customers VALUES(?, ?, ?)"""

    cur.execute(command, (name, last_sub, next_sub))
    cur.close()

    con.commit()

def fetch(limit: int = 300) -> list[any]:
    cur = con.cursor()
    command = f"""SELECT * FROM customers LIMIT {limit}"""
    cur.execute(command)
    result = cur.fetchall()
    cur.close()

    return result

def alter(name: str, last_sub: str, next_sub:str) -> None:
    cur = con.cursor()

    command = f"""UPDATE customers
                SET last_sub = ?,
                    next_sub = ?
                WHERE 
                    name = ?"""
    cur.execute(command, (last_sub, next_sub, name))

    cur.close()
    con.commit()




