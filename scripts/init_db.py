
import os
import sqlite3

os.makedirs("db", exist_ok=True)
con = sqlite3.connect("db/leads.db")
with open("db/schema.sql", encoding="utf-8") as f:
    con.executescript(f.read())
tables = [r[0] for r in con.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
print("Tables in db/leads.db:", tables)
con.close()