"""Mark our own review rows clearly: they are self-review labels, NOT sales feedback. Safe to re-run."""
import sqlite3

PREFIX = "self-review (not sales feedback): "
con = sqlite3.connect("db/leads.db")
cur = con.execute(
    "UPDATE feedback SET notes = ? || COALESCE(notes, '') "
    "WHERE COALESCE(notes, '') NOT LIKE 'self-review%'", (PREFIX,))
con.commit()
print("Rows relabelled:", cur.rowcount)
print("Total feedback rows:", con.execute("SELECT COUNT(*) FROM feedback").fetchone()[0])
con.close()