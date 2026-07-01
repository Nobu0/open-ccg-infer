import ast
import re
import sqlite3
from wcwidth import wcwidth

def visualize_pos_and_boxes(conn, act_id, lang, width=120):
    cur = conn.cursor()

    # pos_tbl の語列
    cur.execute("""
        SELECT src_id, word, line_num
        FROM pos_tbl
        WHERE act_id=? AND lang=?
        ORDER BY src_id
    """, (act_id,lang,))
    pos = cur.fetchall()

    # box_tbl の BOX
    cur.execute("""
        SELECT start_id, end_id
        FROM box_tbl
        WHERE act_id=? AND lang=?
        ORDER BY start_id
    """, (act_id,lang,))
    boxes = cur.fetchall()

    # BOX マーク配列
    max_id = pos[-1][0]
    mark = [" "] * (max_id + 1)
    for s, e in boxes:
        for i in range(s, e+1):
            mark[i] = "#"

    print(f"\n=== act_id={act_id} POS + BOX Visualization ===\n")

    line_words = ""
    line_marks = ""
    current_width = 0
    plno = 0
    for sid, word, lno in pos:
        if plno != lno:
          print(line_marks)
          print(line_words)
          print()
          line_words = ""
          line_marks = ""
          current_width = 0
          
        plno = lno            
        w = word + " "
        m = mark[sid]

        # 表示幅を計算
        w_width = sum(wcwidth(c) for c in w)

        # 行幅を超えたら改行
        if current_width + w_width > width:
            print(line_marks)
            print(line_words)
            print()
            line_words = ""
            line_marks = ""
            current_width = 0

        # 語を追加
        line_words += w
        line_marks += m * w_width
        current_width += w_width

    # 最後の行
    if line_words:
        print(line_marks)
        print(line_words)
        #print()

def visualize_pos_and_boxes_fast(conn, act_id, lang, width=120):
    cur = conn.cursor()

    # pos_tbl の語列
    cur.execute("""
        SELECT src_id, word, line_num
        FROM pos_tbl
        WHERE act_id=? AND lang=?
        ORDER BY src_id
    """, (act_id, lang))
    pos = cur.fetchall()

    # box_tbl の BOX
    cur.execute("""
        SELECT start_id, end_id
        FROM box_tbl
        WHERE act_id=? AND lang=?
        ORDER BY start_id
    """, (act_id, lang))
    boxes = cur.fetchall()

    # 1. BOX マークを O(N) で作る
    max_id = pos[-1][0]
    mark = [0] * (max_id + 2)

    for s, e in boxes:
        mark[s] += 1
        mark[e+1] -= 1

    # prefix sum → covered array
    for i in range(1, len(mark)):
        mark[i] += mark[i-1]

    covered = ["#" if mark[i] > 0 else " " for i in range(max_id + 1)]

    # 2. wcwidth をキャッシュ
    width_cache = {}
    def wlen(w):
        if w not in width_cache:
            width_cache[w] = sum(wcwidth(c) for c in w)
        return width_cache[w]

    print(f"\n=== act_id={act_id} POS + BOX Visualization (FAST) ===\n")

    line_words = ""
    line_marks = ""
    current_width = 0
    plno = None

    for sid, word, lno in pos:
        if plno is not None and plno != lno:
            print(line_marks)
            print(line_words)
            print()
            line_words = ""
            line_marks = ""
            current_width = 0

        plno = lno
        w = word + " "
        m = covered[sid]
        w_width = wlen(w)

        if current_width + w_width > width:
            print(line_marks)
            print(line_words)
            print()
            line_words = ""
            line_marks = ""
            current_width = 0

        line_words += w
        line_marks += m * w_width
        current_width += w_width

    if line_words:
        print(line_marks)
        print(line_words)

conn = sqlite3.connect("db/ccgDB.sqlite")

for i in range(10,11):
  print(f"#********* Act id= {i}  *****************#")
  visualize_pos_and_boxes_fast(conn, i, 2, width=100)
