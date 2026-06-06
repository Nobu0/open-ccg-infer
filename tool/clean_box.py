import sqlite3
from collections import defaultdict

def clean_302(db, act_id, lang):
    cur = db.cursor()

    # 302 の BOX を取得
    cur.execute("""
        SELECT box_id, start_id, end_id, content
        FROM box_tbl
        WHERE act_id=? AND lang=? AND class_id=302
        ORDER BY start_id, end_id
    """, (act_id, lang,))

    rows = cur.fetchall()

    # (box_id, s, e, text)
    boxes = [(bid, s, e, text) for (bid, s, e, text) in rows]

    # 長さ降順でソート
    boxes_sorted = sorted(boxes, key=lambda x: (-(x[2]-x[1]), x[1]))

    keep = []
    delete = []

    for bid, s, e, text in boxes_sorted:
        # すでに keep にある最大句に含まれるなら削除
        if any(s >= ks and e <= ke for (_, ks, ke, _) in keep):
            delete.append(bid)
        else:
            keep.append((bid, s, e, text))

    BATCH = 100
    print(f"act_id={act_id}, len={len(delete)}")
    for i in range(0, len(delete), BATCH):
        batch = delete[i:i+BATCH]
        placeholders = ",".join("?" for _ in batch)
        cur.execute(f"DELETE FROM box_tbl WHERE box_id IN ({placeholders})", batch)
        print(f"act_id={act_id}, len={len(batch)}")
        db.commit()
    """
    # 削除実行
    if delete:
        print(f"act_id={act_id}, len={len(delete)}")
        cur.execute(
            f"DELETE FROM box_tbl WHERE box_id IN ({','.join(['?']*len(delete))})",
            delete
        )
        db.commit()
    """
    return keep, delete

def clean_301(db, act_id, lang):
    cur = db.cursor()

    # 301 の候補を取得
    cur.execute("""
        SELECT box_id, start_id, end_id, content
        FROM box_tbl
        WHERE act_id=? AND lang=? AND class_id=301
        ORDER BY start_id, end_id
    """, (act_id, lang))
    rows = cur.fetchall()

    delete_ids = []
    seen = set()

    for box_id, s, e, text in rows:

        key = (s, e, text)

        # 重複削除
        if key in seen:
            delete_ids.append(box_id)
            continue
        seen.add(key)

        # 2文字以下は削除
        if len(text) <= 2:
            delete_ids.append(box_id)
            continue

        # 括弧語は削除
        if "（" in text or "）" in text:
            delete_ids.append(box_id)
            continue

        # 形容詞（〜的）は削除
        if text.endswith("的"):
            delete_ids.append(box_id)
            continue

        # 年/月/日を含む途中切れ
        if any(x in text for x in ["年", "月", "日"]) and len(text) <= 4:
            delete_ids.append(box_id)
            continue

        # 記号で終わる
        if not text[-1].isalnum():
            delete_ids.append(box_id)
            continue

    # バッチ削除
    BATCH = 100
    print(f"act_id={act_id}, len={len(delete_ids)}")
    for i in range(0, len(delete_ids), BATCH):
        batch = delete_ids[i:i+BATCH]
        placeholders = ",".join("?" for _ in batch)
        cur.execute(f"DELETE FROM box_tbl WHERE box_id IN ({placeholders})", batch)
        print(f"act_id={act_id}, len={len(batch)}")

    db.commit()

    return delete_ids

def xxxclean_301(db, act_id, lang):
    cur = db.cursor()

    # 302/303 の最大名詞句を取得（301 が部分句なら削除するため）
    cur.execute("""
        SELECT start_id, end_id
        FROM box_tbl
        WHERE act_id=? AND lang=? AND class_id IN (302, 303)
    """, (act_id, lang))
    rel_nps = [(s, e) for (s, e) in cur.fetchall()]

    # 301 の候補を取得
    cur.execute("""
        SELECT box_id, start_id, end_id, content
        FROM box_tbl
        WHERE act_id=? AND lang=? AND class_id=301
    """, (act_id, lang))
    rows = cur.fetchall()

    delete_ids = []

    for box_id, s, e, text in rows:

        # 302/303 に含まれるなら削除（部分句）
        if any(s >= ss and e <= ee for (ss, ee) in rel_nps):
            delete_ids.append(box_id)
            continue

        # 2文字以下は削除（誤抽出）
        if len(text) <= 2:
            delete_ids.append(box_id)
            continue

        # 括弧語は削除
        if "（" in text or "）" in text:
            delete_ids.append(box_id)
            continue

        # 名詞で終わらない（ひらがな・カタカナ・漢字以外）
        if not text[-1].isalnum():
            delete_ids.append(box_id)
            continue

        # 「年六月」「日法律」などの途中切れ
        if any(x in text for x in ["年", "月", "日"]) and len(text) <= 4:
            delete_ids.append(box_id)
            continue

        # 形容詞（歴史的など）は削除
        if text.endswith("的"):
            delete_ids.append(box_id)
            continue

    # 削除実行
    BATCH = 100
    print(f"act_id={act_id}, len={len(delete_ids)}")
    for i in range(0, len(delete_ids), BATCH):
        batch = delete_ids[i:i+BATCH]
        placeholders = ",".join("?" for _ in batch)
        cur.execute(f"DELETE FROM box_tbl WHERE box_id IN ({placeholders})", batch)
        print(f"act_id={act_id}, len={len(batch)}")
        db.commit()

    return delete_ids

conn = sqlite3.connect("db/ccgDB.sqlite")

for i in range(1,635):
  print(f"act_id={i}")
  clean_301(conn, i, 1)
  #clean_302(conn, i, 1)
