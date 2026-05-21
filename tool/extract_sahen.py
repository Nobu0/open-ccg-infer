import sqlite3
import os
import re

conn = sqlite3.connect("db/sahen.sqlite")
cur = conn.cursor()

#cur.execute("DELETE FROM sah_tbl")
cur.execute("CREATE TABLE IF NOT EXISTS sah_tbl (word TEXT PRIMARY KEY)")
conn.commit()

sahen = set()
for i in range(1, 635):
    file = f"../act-monad/data/tsv/ja2/src_{i}.txt"
    if not os.path.exists(file):
      continue

    with open(file, encoding="utf-8") as f:
        for line in f:
            cols = line.strip().split()
            if len(cols) < 9:
                continue

            surface = cols[6]
            pos = cols[8]
            if len(cols[6]) > 0:
              surface = "".join(re.findall(r'^[（]?([一-龠々]+)[）]?$', cols[6]))
              print(f"surface = {surface},pos = {pos}")
              if len(surface)> 0:             
                if pos.startswith("名詞") and "サ変" in pos:
                    sahen.add(surface)

for w in sahen:
    #print(f"word = {w}")
    cur.execute("INSERT OR IGNORE INTO sah_tbl (word) VALUES (?)", (w,))

conn.commit()
conn.close()

