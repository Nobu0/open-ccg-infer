import sqlite3
import subprocess
import json

conn = sqlite3.connect("db/ccgDB.sqlite")
cur = conn.cursor()
cur.execute("SELECT content FROM box_tbl WHERE box_id=1")
content = cur.fetchone()[0]

cmd = ["swipl", "-s", "prolog/ccg_db.pl", "-g", f"run('{content}')", "-t", "halt"]
subprocess.run(cmd)
