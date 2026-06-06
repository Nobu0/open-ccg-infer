import sqlite3

import sqlite3

def generate_sixgram(conn, act_id=None, limit=None):
    cur = conn.cursor()

    # pos_tbl を取得
    if act_id is None:
        cur.execute("SELECT act_id, src_id, word FROM pos_tbl ORDER BY act_id, src_id")
    else:
        cur.execute("SELECT act_id, src_id, word FROM pos_tbl WHERE act_id=? ORDER BY src_id", (act_id,))
    print("end select")
    rows = cur.fetchall()

    # act_id ごとに処理
    from collections import defaultdict

    # act_id → [words]
    act_words = defaultdict(list)
    for act, sid, w in rows:
        act_words[act].append((sid, w))

    result = []

    for act, seq in act_words.items():
        # seq = [(src_id, word), ...]
        words = [w for _, w in seq]
        src_ids = [sid for sid, _ in seq]

        # 4-gram を作る
        fg = []
        for i in range(len(words) - 3):
            fg.append((i, words[i:i+4]))  # (index, [w1,w2,w3,w4])

        # 4+4-2 → 6-gram を作る
        sixgrams = defaultdict(int)

        for i, g1 in fg:
            w1 = g1
            tail = tuple(w1[2:4])  # 末尾2語

            # tail が一致する g2 を探す
            for j, g2 in fg:
                if j <= i:
                    continue
                if tuple(g2[0:2]) == tail:
                    # 6-gram = w1[0:4] + g2[2:4]
                    six = w1 + g2[2:4]
                    sixgrams[tuple(six)] += 1

        # 結果を整形
        for six, cnt in sixgrams.items():
            result.append({
                "act_id": act,
                "sixgram": list(six),
                "count": cnt
            })

    # limit があれば適用
    if limit:
        result = result[:limit]

    return result

DB = "db/ccgDB.sqlite"

if __name__ == "__main__":
  conn = sqlite3.connect(DB)
  #rows = generate_sixgram(conn)
  rows = generate_sixgram(conn, act_id=1, limit=50)

  for r in rows:
      print(r["sixgram"])

  conn.close()

  print("[DB] N-Gram.")
  exit()

  # ここで人間が確認して OK なら INSERT
  cur = conn.cursor()
  for r in rows:
      cur.execute("""
          INSERT INTO box_tbl (act_id, start_id, end_id, content, class_id)
          VALUES (?, ?, ?, ?, ?)
      """, (
          r["act_id"],
          r["start_id"],
          r["start_id"] + 5,
          r["sixgram"],
          100  # class_id は仮
      ))

  conn.commit()
  conn.close()

  print("[DB] N-Gram.")
