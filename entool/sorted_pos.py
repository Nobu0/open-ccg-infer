import ast
import re
import ast

def normalize_tuple(t):
    obj = ast.literal_eval(t)
    if isinstance(obj, tuple):
        return obj
    if isinstance(obj, str):
        return (obj,)
    raise ValueError("Unexpected tuple format: " + t)


def load_pos_pattern_file(path):
    data = {}
    current_key = None

    with open(path, encoding="utf-8") as f:
        for line in f:
            raw = line.rstrip("\n")

            # --- ① タプル行（行頭が "(" の場合のみ） ---
            if raw.startswith("("):
                # 例: ('NN',)  1871
                # 左側のタプル部分と右側の数字を分離
                left, right = raw.split(")", 1)
                tuple_str = left + ")"              # ('NN',)
                count_str = right.strip()           # 1871

                key = normalize_tuple(tuple_str)
                count = int(count_str)

                data[key] = {
                    "count": count,
                    "samples": []
                }
                current_key = key
                continue

            # --- ② サンプル行（行頭がスペース） ---
            if raw.startswith(" "):
                # 例: "    3 ['technology']"
                stripped = raw.strip()
                num, arr = stripped.split(" ", 1)
                scount = int(num)
                tokens = ast.literal_eval(arr)
                data[current_key]["samples"].append((scount, tokens))
                continue

            # --- ③ それ以外は無視 ---
            # （空行など）
            continue

    return data

def sort_by_pos_tuple(data):
    # 品詞タプルを辞書順でソート
    return dict(sorted(data.items(), key=lambda x: x[0]))

dat = load_pos_pattern_file("output.txt")
sorted_data = sort_by_pos_tuple(dat)

for pos_tuple, info in sorted_data.items():
    print(pos_tuple, info["count"])
    for sc, toks in info["samples"][:-1]:
        print("   ", sc, toks)
    print()
