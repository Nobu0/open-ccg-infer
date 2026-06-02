import sqlite3

DB = "db/ccgDB.sqlite"

#def record_overlap_history(conn, act_id, name, desc):
def insert_history(conn, lang, act_id, name, desc):

    cur = conn.cursor()

    # pos の総数
    cur.execute("SELECT COUNT(*) FROM pos_tbl WHERE act_id=?", (act_id,))
    all_pos = cur.fetchone()[0]

    # BOX の総数
    cur.execute("SELECT COUNT(*) FROM box_tbl WHERE act_id=?", (act_id,))
    box_cnt = cur.fetchone()[0]

    # BOX の平均幅
    cur.execute("""
        SELECT AVG(end_id - start_id + 1)
        FROM box_tbl
        WHERE act_id=?
    """, (act_id,))
    box_ave = cur.fetchone()[0] or 0

    # 重なり検出
    cur.execute("""
        SELECT 
            A.box_id, B.box_id,
            A.start_id, A.end_id,
            B.start_id, B.end_id
        FROM box_tbl A
        JOIN box_tbl B
          ON A.act_id = B.act_id
         AND A.box_id < B.box_id
         AND A.start_id <= B.end_id
         AND B.start_id <= A.end_id
        WHERE A.act_id=?
    """, (act_id,))

    overlaps = cur.fetchall()

    # 重なり幅の合計
    total_overlap_width = 0

    for box1, box2, a_s, a_e, b_s, b_e in overlaps:
        overlap = min(a_e, b_e) - max(a_s, b_s) + 1
        if overlap > 0:
            total_overlap_width += overlap

    # 重なり率（全 pos に対する割合）
    overlap_rate = (total_overlap_width / all_pos * 100) if all_pos else 0

    # his_box_tbl に記録
    cur.execute("""
        INSERT INTO his_box_tbl
            (act_id, name, desc, lang, all_pos, box_cnt, box_ave, box_hed, box_ovlp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (act_id, name, desc, lang, all_pos, box_cnt, box_ave, 0, overlap_rate))

    conn.commit()

    return overlap_rate


if __name__ == "__main__":
  conn = sqlite3.connect(DB)
  #cur = conn.cursor()
  insert_history(conn, 0, 1, "テスト", "cd")

  conn.close()

  print("[DB] History.")
