import sqlite3

def assign_ccg_for_act(db, act_id, lang):
    cur = db.cursor()

    # 1. BOX を取得
    cur.execute("""
        SELECT box_id, class_id, box_type, content
        FROM box_tbl
        WHERE act_id=? AND lang=?
        ORDER BY start_id
    """, (act_id, lang,))

    rows = cur.fetchall()
    print(act_id)
    for box_id, class_id, pos_seq, text in rows:
        print(box_id, class_id, pos_seq)
        # pos_seq は ('nn','nn') のようなタプル
        pos = eval(pos_seq) if isinstance(pos_seq, str) else pos_seq

        # 2. class_id に応じて CCG カテゴリを決定
        if class_id == 301:
            ccg = "NP"  # 純名詞句

        elif class_id == 302:
            ccg = "NP/NP"  # 連体修飾（の）

        elif class_id == 303:
            ccg = "NP"  # アドレス句・名詞化述語句

        elif class_id == 304:
            ccg = "NP"  # その他の名詞句

        else:
            ccg = None  # それ以外は無視

        # 3. CCG カテゴリを保存
        if ccg:
            cur.execute("""
                UPDATE box_tbl
                SET ccg = ?
                WHERE box_id = ?
            """, (ccg, box_id))

    db.commit()

conn = sqlite3.connect("db/ccgDB.sqlite")

for i in range(1,2):
  print(i)
  assign_ccg_for_act(conn, i, 1)

conn.close()