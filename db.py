import sqlite3 as sql


# Makes the main connection
con = sql.connect("main.db")

def check() -> None:
    """Checks for the tables inside the db"""
    cur = con.cursor()

    command = """CREATE TABLE IF NOT EXISTS customers (
        name TEXT PRIMARY KEY,
        last_sub TEXT,
        next_sub TEXT)"""

    cur.execute(command)
    cur.close()

    con.commit()

def add(name: str, last_sub: str, next_sub: str) -> None:
    """Adds a customer to the db
    Parameters:
    - Name (str): name of the user
    - Last_sub (str): last sub date
    - Next_sub (str): next sub date
    Errors:
    - A sqlite IntegrityError is name is already in db"""

    cur = con.cursor()
    command = """INSERT INTO customers VALUES(?, ?, ?)"""

    cur.execute(command, (name, last_sub, next_sub))
    cur.close()

    con.commit()

def fetch(limit: int = 300) -> list[any]:
    """Fetch customers form the db
    Parameters:
    - Limit (int): limit on how many customers returned
    Return:
    - List (any): A List of the customers names, last sub and next sub"""

    cur = con.cursor()

    command = f"""SELECT * FROM customers LIMIT {limit}"""
    cur.execute(command)

    result = cur.fetchall()
    cur.close()

    return result

def alter(name: str, last_sub: str, next_sub:str) -> None:
    """Changes a the last and next sub dates in db
    Parameters:
    - Name (str): the name of the customer
    - Last_sub (str): the new last sub date
    - Next_sub (str): the new next sub date
    """
    cur = con.cursor()

    command = f"""UPDATE customers
                SET last_sub = ?,
                    next_sub = ?
                WHERE 
                    name = ?"""
    cur.execute(command, (last_sub, next_sub, name))

    cur.close()
    con.commit()




