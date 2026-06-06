import sqlite3
from collections import defaultdict

def batch_box_with_history(conn, act_id=None, lang=1, name="BOX batch", desc="pos_box_tbl patterns"):
    cur = conn.cursor()

    # -----------------------------
    # 1. pos_box_tbl からパターン取得
    # -----------------------------
    cur.execute("""
        SELECT pat_tags, pat_len, class_id
        FROM pos_box_tbl
        WHERE lang=?
        ORDER BY priority ASC
    """, (lang,))
    patterns = cur.fetchall()

    # -----------------------------
    # 2. pos_tbl から品詞列を取得
    # -----------------------------
    if act_id is None:
        cur.execute("SELECT act_id, src_id, pos, word FROM pos_tbl ORDER BY act_id, src_id")
    else:
        cur.execute("SELECT act_id, src_id, pos, word FROM pos_tbl WHERE act_id=? ORDER BY src_id", (act_id,))

    rows = cur.fetchall()

    pos_map = defaultdict(list)
    for act, sid, tag, word in rows:
        pos_map[act].append((sid, tag, word))

    # -----------------------------
    # 3. BOX 化処理
    # -----------------------------
    total_box = 0
    total_width = 0
    total_overlap = 0

    for act, seq in pos_map.items():
        tags = [t for _, t, _ in seq]
        words = [w for _, _, w in seq]
        src_ids = [sid for sid, _, _ in seq]

        act_box_count = 0
        act_width_sum = 0
        print(f"act= {act}, seq={seq}")
        for pat_tags, pat_len, class_id in patterns:
            pat = pat_tags.split(",")

            for i in range(len(tags) - pat_len + 1):
                if tags[i:i+pat_len] == pat:
                    start_id = src_ids[i]
                    end_id   = src_ids[i + pat_len - 1]
                    content  = "".join(words[i:i+pat_len])

                    cur.execute("""
                        INSERT INTO box_tbl (act_id, lang, start_id, end_id, content, class_id)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (act, lang, start_id, end_id, content, class_id))

                    act_box_count += 1
                    act_width_sum += (end_id - start_id + 1)

        # 法令単位の統計
        if act_box_count > 0:
            total_box += act_box_count
            total_width += act_width_sum

    conn.commit()

    # -----------------------------
    # 4. BOX 統計の計算
    # -----------------------------
    if total_box > 0:
        box_ave = total_width / total_box
    else:
        box_ave = 0

    # 重なり率（簡易版：BOX 数 / pos 数）
    cur.execute("SELECT COUNT(*) FROM pos_tbl")
    all_pos = cur.fetchone()[0]

    if all_pos > 0:
        box_ovlp = total_box / all_pos
    else:
        box_ovlp = 0

    # 位置率（BOX の start_id の平均位置）
    cur.execute("SELECT AVG(start_id) FROM box_tbl")
    avg_pos = cur.fetchone()[0] or 0
    box_hed = (avg_pos / all_pos) * 100 if all_pos > 0 else 0

    # -----------------------------
    # 5. his_box_tbl に履歴登録
    # -----------------------------
    cur.execute("""
        INSERT INTO his_box_tbl
        (act_id, name, desc, lang, all_pos, box_cnt, box_ave, box_hed, box_ovlp, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        act_id if act_id else -1,
        name,
        desc,
        lang,
        all_pos,
        total_box,
        box_ave,
        box_hed,
        box_ovlp,
        1
    ))

    conn.commit()

    print("BOX 化完了:", total_box, "件")
    print("平均幅:", box_ave)
    print("重なり率:", box_ovlp)
    print("位置率:", box_hed)


conn = sqlite3.connect("db/ccgDB.sqlite")

batch_box_with_history(
    conn,
    act_id=None,          # 全法令
    lang=1,               # 日本語
    name="ADDR BOX 初期化",
    desc="pos_box_tbl に基づくアドレス句 BOX 化"
)
