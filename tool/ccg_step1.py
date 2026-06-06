import sqlite3  # 例として SQLite。MySQL でも同様の構造で書けます。

def skeletonize_with_np(pos_line, boxes):
    """
    pos_line: [(token_id, pos, word), ...]
    boxes: [(start_id, end_id), ...]
    """

    n = len(pos_line)
    mark = [0] * n

    # token_id → index 変換
    token_index = {tok_id: idx for idx, (tok_id, pos, word) in enumerate(pos_line)}

    # NP BOX の範囲をマーキング
    for (s, e) in boxes:
        for tid in range(s, e + 1):
            if tid in token_index:
                mark[token_index[tid]] = 1

    result = []
    i = 0
    while i < n:
        if mark[i] == 1:
            result.append("NP")
            while i < n and mark[i] == 1:
                i += 1
        else:
            result.append(pos_line[i][2])  # word
            i += 1

    return " ".join(result)

import sqlite3

def run_skeleton(act_id):
    conn = sqlite3.connect("db/ccgDB.sqlite")
    cur = conn.cursor()

    # 1. pos_tbl を取得
    cur.execute("""
        SELECT src_id, pos, word
        FROM pos_tbl
        WHERE act_id = ? AND lang = 1
        ORDER BY src_id
    """, (act_id,))
    pos_line = cur.fetchall()

    # 2. NP BOX を取得
    cur.execute("""
        SELECT start_id, end_id
        FROM box_tbl
        WHERE act_id = ?
          AND class_id = 100 AND lang = 1
        ORDER BY start_id, end_id
    """, (act_id,))
    boxes = cur.fetchall()

    # 3. スケルトン化
    skeleton = skeletonize_with_np(pos_line, boxes)

    conn.close()
    return skeleton

# 実行例
act_id = 1
skel = run_skeleton(act_id)
print(skel)

