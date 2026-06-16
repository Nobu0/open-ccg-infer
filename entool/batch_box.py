import sqlite3
from collections import defaultdict

from collections import defaultdict
import sys



def batch_box(conn, act_id=None, lang=1,class_id=304,
                           name="BOX batch", desc="pos_box_tbl patterns",
                           batch_size=1000):

    cur = conn.cursor()

    # ----------------------------------------
    # 1. pos_box_tbl のパターンを一度だけ取得
    #    → 長さ別にグループ化し、ハッシュ照合用に整形
    # ----------------------------------------
    cur.execute("""
        SELECT pat_tags, pat_len, class_id
        FROM pos_box_tbl
        WHERE lang=? and class_id=?
        ORDER BY priority ASC
    """, (lang,class_id,))

    patterns_by_len = defaultdict(lambda: defaultdict(list))
    # patterns_by_len[pat_len][tuple(tags)] = [class_id, class_id, ...]

    for pat_tags, pat_len, class_idx in cur.fetchall():
        pat = tuple(pat_tags.split(","))
        patterns_by_len[pat_len][pat].append(class_idx)

    # ----------------------------------------
    # 2. 対象 act_id の一覧を取得
    # ----------------------------------------
    if act_id is None:
        cur.execute("SELECT DISTINCT act_id FROM pos_tbl ORDER BY act_id")
        act_list = [row[0] for row in cur.fetchall()]
    else:
        act_list = [act_id]

    total_box = 0
    total_width = 0

    # ----------------------------------------
    # 3. act_id ごとに BOX 化
    # ----------------------------------------
    for act in act_list:
        print(f"act_id = {act}")
        # pos_tbl を act_id ごとに読み込む
        cur.execute("""
            SELECT src_id, pos, word
            FROM pos_tbl
            WHERE act_id = ?
            ORDER BY src_id
        """, (act,))
        rows = cur.fetchall()
        if not rows:
            continue

        src_ids = [sid for (sid, _, _) in rows]
        tags    = [pos for (_, pos, _) in rows]
        words   = [w   for (_, _, w)   in rows]

        n = len(tags)
        act_box_count = 0
        act_width_sum = 0

        insert_buffer = []

        # -------------------------
        # パターン長ごとにローリングウィンドウで照合
        # -------------------------
        for pat_len, pat_dict in patterns_by_len.items():
            if n < pat_len:
                continue

            # 最初のウィンドウ
            window = tuple(tags[0:pat_len])

            # 位置 0 のチェック
            if window in pat_dict:
                for class_id in pat_dict[window]:
                    start_id = src_ids[0]
                    end_id   = src_ids[pat_len - 1]
                    content  = " ".join(words[0:pat_len])

                    insert_buffer.append(
                        (act, lang, start_id, end_id, content, class_id, f"{window}")
                    )
                    act_box_count += 1
                    act_width_sum += (end_id - start_id + 1)

            # 位置 1 以降のローリング
            for i in range(1, n - pat_len + 1):
                # window = window[1:] + (tags[i + pat_len - 1],)
                # 上の書き方でもよいが、明示的に書いておく
                window = (*window[1:], tags[i + pat_len - 1])

                if window in pat_dict:
                    for class_id in pat_dict[window]:
                        start_id = src_ids[i]
                        end_id   = src_ids[i + pat_len - 1]
                        content  = " ".join(words[i:i+pat_len])

                        insert_buffer.append(
                            (act, lang, start_id, end_id, content, class_id, f"{window}")
                        )
                        act_box_count += 1
                        act_width_sum += (end_id - start_id + 1)

                # バッチサイズに達したらまとめて INSERT
                if len(insert_buffer) >= batch_size:
                    cur.executemany("""
                        INSERT OR IGNORE INTO box_tbl
                            (act_id, lang, start_id, end_id, content, class_id, box_type)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, insert_buffer)
                    insert_buffer.clear()

        try:
          # 残りをフラッシュ
          if insert_buffer:
              cur.executemany("""
                  INSERT OR IGNORE INTO box_tbl
                      (act_id, lang, start_id, end_id, content, class_id, box_type)
                  VALUES (?, ?, ?, ?, ?, ?, ?)
              """, insert_buffer)
              insert_buffer.clear()

        except Exception as e:
            print("変換エラー:", insert_buffer, e)

        total_box   += act_box_count
        total_width += act_width_sum

        # act_id 単位で COMMIT
        conn.commit()

    return total_box, total_width


def batch__history(conn, total_box, total_witdh, act_id=None, lang=1, name="BOX batch", desc="pos_box_tbl patterns"):
    cur = conn.cursor()

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

# sys.argvには、実行時の引数が「文字列のリスト」として格納されます
args = sys.argv

print(f"実行ファイル名: {args[0]}")
print(f"第1引数: {args[1]}")

if args[1] == "304":
    
    total_box,total_width = batch_box(
        conn,
        act_id=None,          # 全法令
        lang=2,               # 日本語
        class_id=304,
        name="その他の一般NP",
        desc="pos_box_tbl に基づくアドレス句 BOX 化"
    )

    batch__history(conn,
        total_box,
        total_width,
        act_id=None,
        lang=2,
        name="その他の一般NP",
        desc="pos_box_tbl に基づくアドレス句 BOX 化"
        )

elif args[1] == "305":
    
    total_box,total_width = batch_box(
        conn,
        act_id=None,          # 全法令
        lang=2,               # 日本語
        class_id=305,
        name="固有名詞連結・特殊NP",
        desc="pos_box_tbl に基づくアドレス句 BOX 化"
    )

    batch__history(conn,
        total_box,
        total_width,
        act_id=None,
        lang=2,
        name="固有名詞連結・特殊NP",
        desc="pos_box_tbl に基づくアドレス句 BOX 化"
        )


