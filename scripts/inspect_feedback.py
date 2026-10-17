
import sqlite3

con = sqlite3.connect("db/leads.db")

tables = con.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name
""").fetchall()

print("DATABASE TABLES:")
for (table_name,) in tables:
    print("-", table_name)

print("\nFEEDBACK TABLE SCHEMA:")
try:
    schema = con.execute("PRAGMA table_info(feedback)").fetchall()
    if schema:
        for column in schema:
            print(column)
    else:
        print("Feedback table does not exist yet.")
finally:
    con.close()
