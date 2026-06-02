import ast
import re
import sqlite3


def visualize_boxes(conn, act_id, width=120):
    cur = conn.cursor()

    # pos_tbl の語列を取得
    cur.execute("""
        SELECT src_id, word
        FROM pos_tbl
        WHERE act_id=?
        ORDER BY src_id
    """, (act_id,))
    pos = cur.fetchall()

    # box_tbl の BOX を取得
    cur.execute("""
        SELECT start_id, end_id, content, class_id
        FROM box_tbl
        WHERE act_id=?
        ORDER BY start_id
    """, (act_id,))
    boxes = cur.fetchall()

    # pos の最大 src_id
    max_id = pos[-1][0]

    # BOX のマーク用配列
    mark = [" "] * (max_id + 1)

    for s, e, content, cid in boxes:
        for i in range(s, e+1):
            mark[i] = "#"

    # 可視化出力
    print("=== BOX Visualization for act_id =", act_id, "===")

    line_words = []
    line_marks = []

    for sid, word in pos:
        line_words.append(word)
        line_marks.append(mark[sid])

        if len(line_words) >= width:
            print("".join(line_marks))
            print("".join(line_words))
            print()
            line_words = []
            line_marks = []

    # 最後の行
    if line_words:
        print("".join(line_marks))
        print("".join(line_words))
        print()


def visualize_boxes_with_content(conn, act_id):
    cur = conn.cursor()

    cur.execute("""
        SELECT start_id, end_id, content, class_id
        FROM box_tbl
        WHERE act_id=?
        ORDER BY start_id
    """, (act_id,))
    boxes = cur.fetchall()

    print("=== BOX List for act_id =", act_id, "===")
    for s, e, content, cid in boxes:
        print(f"[{s}-{e}] ({cid}) {content}")

def xxxxvisualize_pos_and_boxes(conn, act_id, width=120):
    cur = conn.cursor()

    # pos_tbl の語列を取得
    cur.execute("""
        SELECT src_id, word
        FROM pos_tbl
        WHERE act_id=?
        ORDER BY src_id
    """, (act_id,))
    pos = cur.fetchall()

    # box_tbl の BOX を取得
    cur.execute("""
        SELECT start_id, end_id, class_id
        FROM box_tbl
        WHERE act_id=?
        ORDER BY start_id
    """, (act_id,))
    boxes = cur.fetchall()

    # pos の最大 src_id
    max_id = pos[-1][0]

    # BOX のマーク用配列
    mark = ["　"] * (max_id + 1)

    for s, e, cid in boxes:
        for i in range(s, e+1):
            mark[i] = "＃"

    print(f"\n=== act_id={act_id} POS + BOX Visualization ===\n")

    line_words = []
    line_marks = []

    for sid, word in pos:
        line_words.append(word)
        line_marks.append(mark[sid])

        if len(line_words) >= width:
            print("".join(line_marks))
            print("".join(line_words))
            print()
            line_words = []
            line_marks = []

    # 最後の行
    if line_words:
        print("".join(line_marks))
        print("".join(line_words))
        print()

from wcwidth import wcwidth

def visualize_pos_and_boxes(conn, act_id, width=120):
    cur = conn.cursor()

    # pos_tbl の語列
    cur.execute("""
        SELECT src_id, word
        FROM pos_tbl
        WHERE act_id=?
        ORDER BY src_id
    """, (act_id,))
    pos = cur.fetchall()

    # box_tbl の BOX
    cur.execute("""
        SELECT start_id, end_id
        FROM box_tbl
        WHERE act_id=?
        ORDER BY start_id
    """, (act_id,))
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

    for sid, word in pos:
        w = word
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
        print()

conn = sqlite3.connect("db/ccgDB.sqlite")

visualize_pos_and_boxes(conn, 1, width=100)
