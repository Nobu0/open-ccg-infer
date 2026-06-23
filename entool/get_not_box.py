import ast
import re
import sqlite3
import time

box_nomap={}

def append_nomap(key, tokens, src):
      sky = tuple(tokens)
      if key not in box_nomap:
        box_nomap[key] = {
              "count": 0,
              "examples": {},
          }
      box_nomap[key]["count"] += 1
      if sky not in box_nomap[key]["examples"]:
        box_nomap[key]["examples"][sky] = {
          "count": 0,
          "text": "",
          "src": ""
        }
      box_nomap[key]["examples"][sky]["count"] += 1  
      box_nomap[key]["examples"][sky]["text"] = tokens
      box_nomap[key]["examples"][sky]["src"] = src

def extract_unboxed_spans(conn, act_id, lang):
    cur = conn.cursor()

    # POS を取得
    cur.execute("""
        SELECT src_id, word, line_num
        FROM pos_tbl
        WHERE act_id=? AND lang=?
        ORDER BY src_id
    """, (act_id, lang))
    pos = cur.fetchall()
    if not pos:
        return []

    # BOX を取得
    cur.execute("""
        SELECT start_id, end_id
        FROM box_tbl
        WHERE act_id=? AND lang=?
        ORDER BY start_id
    """, (act_id, lang))
    boxes = cur.fetchall()

    # POS の最小・最大 src_id を取得
    min_id = pos[0][0]
    max_id = pos[-1][0]

    # prefix-sum 用配列（min_id〜max_id に対応）
    size = max_id - min_id + 3
    mark = [0] * size

    # BOX を mark に反映
    for s, e in boxes:
        s = max(s, min_id)
        e = min(e, max_id)
        mark[s - min_id] += 1
        mark[e - min_id + 1] -= 1

    # prefix sum
    for i in range(1, size):
        mark[i] += mark[i - 1]

    # covered 配列（min_id〜max_id）
    covered = {min_id + i: (1 if mark[i] > 0 else 0)
               for i in range(max_id - min_id + 1)}

    # 未BOX 区間抽出
    spans = []
    i = min_id
    while i <= max_id:
        if covered[i] == 0:
            start = i
            i += 1
            while i <= max_id and covered[i] == 0:
                i += 1
            end = i - 1
            spans.append((start, end))
        else:
            i += 1

    # src_id → (word, line_no)
    pos_dict = {sid: (word, lno) for sid, word, lno in pos}

    results = []
    for s, e in spans:
        # pos_dict に存在する index のみ使用
        words = [pos_dict[i][0] for i in range(s, e + 1) if i in pos_dict]
        if not words:
            continue
        line_no = pos_dict[s][1] if s in pos_dict else pos_dict[e][1]
        results.append({
            "line": line_no,
            "start": s,
            "end": e,
            "text": " ".join(words),
        })

    return results

from collections import Counter, defaultdict

# 単純句（BOX化不要）を除外するためのリスト
SIMPLE_PATTERNS = {
    ("in", "the"), ("of", "the"), ("to", "the"),
    ("for", "the"), ("by", "the"), ("with", "the"),
    ("in",), ("of",), ("to",), ("for",), ("by",), ("with",)
}

def is_simple_phrase(words):
    """単純句（BOX化不要）を除外する"""
    w = tuple(w.lower() for w in words)
    if len(w) <= 2 and w in SIMPLE_PATTERNS:
        return True
    return False

from collections import Counter, defaultdict

# 全 act_id を横断して集計するための外部変数
freq = Counter()
pos_patterns = {}
examples = defaultdict(list)

def analyze_unboxed_spans_for_act(conn, act_id, lang):
    global freq, pos_patterns, examples

    spans = extract_unboxed_spans(conn, act_id, lang)

    # POS 辞書
    cur = conn.cursor()
    cur.execute("""
        SELECT src_id, pos, word
        FROM pos_tbl
        WHERE act_id=? AND lang=?
        ORDER BY src_id
    """, (act_id, lang))
    pos_rows = cur.fetchall()
    pos_dict = {sid: (pos, word) for sid, pos, word in pos_rows}

    for sp in spans:
        s, e = sp["start"], sp["end"]

        # words と pos を復元
        words = []
        poses = []
        for i in range(s, e+1):
            if i in pos_dict:
                pos, word = pos_dict[i]
                words.append(word)
                poses.append(pos)

        if not words:
            continue

        # 単純句の除外
        if is_simple_phrase(words):
            continue

        key = tuple(words)
        freq[key] += 1
        pos_patterns[key] = tuple(poses)

        if len(examples[key]) < 3:
            txt = " ".join(words)
            examples[key].append(txt)
            append_nomap(tuple(poses),words,"")


start_time = time.perf_counter()
conn = sqlite3.connect("db/ccgDB.sqlite")

cur = conn.cursor()
cur.execute("SELECT DISTINCT act_id FROM pos_tbl WHERE lang=2")
acts = [row[0] for row in cur.fetchall()]

for act_id in acts:
    print(f"Processing act_id={act_id}")
    analyze_unboxed_spans_for_act(conn, act_id, 2)
    end_time = time.perf_counter()
    # 所要時間の計算（秒）
    elapsed_time = end_time - start_time
    print(f"所要時間: {elapsed_time:.4f} 秒")
    #if act_id > 5:
    #    break

i = 1
cnt = 0
MX = 10000
with open("output.txt", "w", encoding="utf-8") as f:
    # box_nomap を頻度順に並べてダンプする
    # (key, count) のリストを作る
    data = [(key, box_nomap[key]["count"]) for key in box_nomap]

    # count の降順でソート
    #data_sorted = sorted(data, key=lambda x: x[1], reverse=True)
    data_sorted = sorted(data, key=lambda x: x[0], reverse=True)

    #print("\n=== 未BOXパターン（頻度順） ===\n")

    for key, count in data_sorted[:-1]:
        print(key, f"{count:5d}", file=f)

        # 例文を出す
        examples = box_nomap[key]["examples"]

        # 例文も頻度順に並べる
        ex_sorted = sorted(
            examples.items(),
            key=lambda x: x[1]["count"],
            reverse=True
        )
        mx = 5
        if len(key) > 5:
            mx = 100
        for (tok_tuple, info) in ex_sorted[:mx]:  # 上位5例文
            print(f"{info['count']:5d}", info["text"],file=f)

