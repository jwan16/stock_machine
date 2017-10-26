import sqlite3

conn = sqlite3.connect("db.sqlite3")
c = conn.cursor()

def read_from_db():
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")

read_from_db()