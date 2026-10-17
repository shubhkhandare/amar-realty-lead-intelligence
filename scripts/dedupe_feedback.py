"""Keep ONE self-review row per lead. Prefers rows tagged 'self_...'. Safe to re-run."""
import sqlite3

con = sqlite3.connect("db/leads.db")
rows = con.execute(
    "SELECT feedback_id, lead_id, sales_tag FROM feedback ORDER BY lead_id, feedback_id").fetchall()
print("Feedback rows before:", len(rows))

best = {}                                   # lead_id -> (is_self_tag, feedback_id)
for feedback_id, lead_id, tag in rows:
    is_self = 1 if (tag or "").startswith("self_") else 0
    if lead_id not in best or is_self > best[lead_id][0]:
        best[lead_id] = (is_self, feedback_id)

keep_ids = {fid for _, fid in best.values()}
to_delete = [fid for fid, _, _ in rows if fid not in keep_ids]
con.executemany("DELETE FROM feedback WHERE feedback_id = ?", [(i,) for i in to_delete])
con.commit()

print("Duplicate rows deleted:", len(to_delete))
print("Feedback rows after:", con.execute("SELECT COUNT(*) FROM feedback").fetchone()[0])
print("Leads with more than one row now:",
      con.execute("SELECT COUNT(*) FROM (SELECT lead_id FROM feedback GROUP BY lead_id HAVING COUNT(*) > 1)").fetchone()[0])
con.close()