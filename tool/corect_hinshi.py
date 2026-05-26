import sqlite3
import os
import re

conn = sqlite3.connect("db/hinshi.sqlite")
cur = conn.cursor()

#cur.execute("DELETE FROM sah_tbl")
cur.execute("CREATE TABLE IF NOT EXISTS pos_tbl (pos TEXT PRIMARY KEY)")
conn.commit()

hinshi = set()
for i in range(1, 635):
    file = f"../act-monad/data/tsv/ja2/src_{i}.txt"
    if not os.path.exists(file):
      continue
    #print(f"i = {i}")
    with open(file, encoding="utf-8") as f:
        for line in f:
            cols = line.strip().split()
            if len(cols) < 9:
                continue
            if len(cols) == 10:
              pos = cols[9]
            else:
              pos = cols[8]
            if len(pos) > 0:
              hinshi.add(pos)

list = sorted(hinshi)
for w in list:
    print(f"pos:  {w}")
    cur.execute("INSERT OR IGNORE INTO pos_tbl (pos) VALUES (?)", (w,))

conn.commit()
conn.close()

