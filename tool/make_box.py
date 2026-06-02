import sqlite3

DB = "db/ccgDB.sqlite"
lang = 1
ccg = ""

def make_box_ADDR(act_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # アドレス候補の抽出（例：条・項・号）
    # ※ pos_tbl は絶対に汚さない
    cur.execute("""
        SELECT src_id, word, pos
        FROM pos_tbl
        WHERE act_id = ?
          AND pos IN ('cdhd', 'cd', 'nnt')
        ORDER BY src_id
    """, (act_id,))

    rows = cur.fetchall()
    if not rows:
        print("No ADDR candidates.")
        return

    # 連続範囲を BOX にまとめる
    start = rows[0][0]
    prev = start

    for i in range(1, len(rows)):
        sid = rows[i][0]
        if sid != prev + 1:
            # BOX を確定
            insert_box(conn, act_id, start, prev, "ADDR", 101)
            start = sid
        prev = sid

    # 最後の BOX
    insert_box(conn, act_id, start, prev, "ADDR", 101)

    conn.commit()
    conn.close()


def insert_box(conn, act_id, start_id, end_id, box_type, class_id):
    cur = conn.cursor()

    # content を pos_tbl から再構築
    cur.execute("""
        SELECT word
        FROM pos_tbl
        WHERE src_id BETWEEN ? AND ?
        ORDER BY src_id
    """, (start_id, end_id))

    words = [w[0] for w in cur.fetchall()]
    content = "".join(words)  # 日本語は空白なしが最適

    try:
        cur.execute("""
            INSERT INTO box_tbl
                (act_id, lang, start_id, end_id, box_type, class_id, ccg, content)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (act_id, lang, start_id, end_id, box_type, class_id, ccg, content))
    except sqlite3.IntegrityError:
        # UNIQUE 制約により既存 BOX がある
        print(f"SKIP: BOX already exists {start_id}-{end_id} ({box_type})")

    print(f"BOX ADDR: {start_id}-{end_id} → {content}")


if __name__ == "__main__":
   make_box_ADDR(1)