
import sqlite3
import re


def is_np_box(s, e, pos_line):
    poses = [pos for (_, pos, _) in pos_line[s:e+1]]

    # 節や動詞句を除外
    if any(p.startswith('V') for p in poses):
        return False

    # 名詞句の基本条件
    if poses[0].startswith('NN') and poses[-1].startswith('NN'):
        return True

    return False


def show_ccg_skeleton(db, act_id, lang=1):
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute("""
        SELECT p.word, c.ccg
        FROM pos_tbl p
        JOIN ccg_token_tbl c ON p.src_id = c.src_id
        WHERE p.act_id = ?
          AND p.lang = ?
        ORDER BY p.src_id
    """, (act_id, lang))

    rows = cur.fetchall()
    conn.close()

    line = " ".join(
        f"{w}/{cat}" for (w, cat) in rows
    )
    print(line)

def merge_np_sequence(tokens):
    """
    tokens: [(word, ccg, class_id, pos_seq), ...]
    """

    merged = []
    buffer_words = []
    buffer_pos = []

    for word, ccg, class_id, pos_seq in tokens:

        # 301（NP_SIMPLE）だけ結合対象
        if class_id == 301:
            buffer_words.append(word)
            buffer_pos.extend(pos_seq)
            continue

        # 301 以外が来たら、バッファを吐き出す
        if buffer_words:
            merged.append(("".join(buffer_words), "NP", 301, tuple(buffer_pos)))
            buffer_words = []
            buffer_pos = []

        # 301 以外はそのまま追加
        merged.append((word, ccg, class_id, pos_seq))

    # 最後のバッファ処理
    if buffer_words:
        merged.append(("".join(buffer_words), "NP", 301, tuple(buffer_pos)))

    return merged

def apply_ccg(tokens):
    """
    tokens: [(word, ccg, class_id, pos_seq), ...]
    """

    changed = True
    while changed:
        changed = False
        new_tokens = []
        i = 0

        while i < len(tokens):
            word, ccg, class_id, pos_seq = tokens[i]

            # NP/NP + NP → NP
            if ccg == "NP/NP" and i + 1 < len(tokens):
                next_word, next_ccg, next_class, next_pos = tokens[i+1]

                if next_ccg == "NP":
                    # 結合
                    merged_word = word + next_word
                    merged_pos = pos_seq + next_pos
                    new_tokens.append((merged_word, "NP", 301, merged_pos))
                    i += 2
                    changed = True
                    continue

            # 結合しない場合はそのまま
            new_tokens.append(tokens[i])
            i += 1

        tokens = new_tokens

    return tokens


def apply_ccg_for_act(db, act_id, lang):
    cur = db.cursor()

    # 1. BOX を start_id 順に取得
    cur.execute("""
        SELECT box_id, content, ccg, class_id, box_type, start_id, end_id
        FROM box_tbl
        WHERE act_id=? AND lang=?
        ORDER BY start_id
    """, (act_id, lang))

    rows = cur.fetchall()

    # 2. ノード化
    nodes = []
    for box_id, content, ccg, class_id, pos_seq, start_id, end_id in rows:
        pos = cnv_poslist(pos_seq)
        #pos = eval(pos_seq) if isinstance(pos_seq, str) else pos_seq
        nodes.append({
            "box_id": box_id,
            "label": ccg,
            "word": content,
            "class_id": class_id,
            "pos_seq": pos,
            "start": start_id,
            "end": end_id,
            "children": []
        })

    # 3. CCG 結合ループ
    changed = True
    while changed:
        changed = False
        new_nodes = []
        i = 0

        while i < len(nodes):
            node = nodes[i]

            # NP/NP + NP → NP
            if node["label"] == "NP/NP" and i + 1 < len(nodes):
                right = nodes[i+1]

                if right["label"] == "NP":
                    merged = {
                        "box_id": None,
                        "label": "NP",
                        "word": node["word"] + right["word"],
                        "class_id": 301,
                        "pos_seq": node["pos_seq"] + right["pos_seq"],
                        "start": node["start"],
                        "end": right["end"],
                        "children": [node, right]
                    }
                    new_nodes.append(merged)
                    i += 2
                    changed = True
                    continue

            # 結合しない場合
            new_nodes.append(node)
            i += 1

        nodes = new_nodes

    # 4. 結果を返す（または DB に保存）
    return nodes

def build_ccg_tree(nodes):
    """
    nodes: apply_ccg_for_act の出力
           [{"label": "NP", "word": "...", "children": [...], ...}, ...]
    """

    changed = True
    while changed:
        changed = False
        new_nodes = []
        i = 0

        while i < len(nodes):
            node = nodes[i]

            # NP/NP + NP → NP
            if node["label"] == "NP/NP" and i + 1 < len(nodes):
                right = nodes[i+1]

                if right["label"] == "NP":
                    merged = {
                        "label": "NP",
                        "word": node["word"] + right["word"],
                        "start": node["start"],
                        "end": right["end"],
                        "children": [node, right]
                    }
                    new_nodes.append(merged)
                    i += 2
                    changed = True
                    continue

            # 結合しない場合
            new_nodes.append(node)
            i += 1

        nodes = new_nodes

    return nodes

def save_ccg_tree(db, act_id, lang, tree_nodes):
    cur = db.cursor()

    for t in tree_nodes:
        cur.execute("""
            INSERT INTO ccg_tree_tbl(act_id, lang, label, word, start_id, end_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (act_id, lang, t["label"], t["word"], t["start"], t["end"]))

    db.commit()

def print_ccg_tree(node, indent=""):
    """
    node: {"label":..., "word":..., "children":[...]}
    """
    # ノードの表示
    print(f"{indent}{node['label']}  「{node['word']}」")

    # 子ノードがあれば再帰
    for child in node.get("children", []):
        print_ccg_tree(child, indent + "    ")

def visualize_ccg_forest(nodes):
    for i, node in enumerate(nodes, 1):
        print(f"\n=== TREE {i} ===")
        print_ccg_tree(node)

def apply_ccg_visualize(tokens):
    """
    tokens: [(word, ccg, class_id, pos_seq), ...]
    """

    log = []  # ← 可視化ログ

    changed = True
    while changed:
        changed = False
        new_tokens = []
        i = 0

        while i < len(tokens):
            word, ccg, class_id, pos_seq = tokens[i]

            # NP/NP + NP → NP
            if ccg == "NP/NP" and i + 1 < len(tokens):
                next_word, next_ccg, next_class, next_pos = tokens[i+1]

                if next_ccg == "NP":
                    merged_word = word + next_word
                    merged_pos = pos_seq + next_pos

                    # ★ 可視化ログを追加
                    log.append(
                        f"{ccg}:{word}  ×  {next_ccg}:{next_word}  →  NP:{merged_word}"
                    )

                    new_tokens.append((merged_word, "NP", 301, merged_pos))
                    i += 2
                    changed = True
                    continue

            new_tokens.append(tokens[i])
            i += 1

        tokens = new_tokens

    return tokens, log


def apply_ccg_and_save_log(db, act_id, lang, tokens):
    """
    tokens: [(word, ccg, class_id, pos_seq), ...]
    """

    cur = db.cursor()
    step_no = 1
    log_entries = []

    changed = True
    while changed:
        changed = False
        new_tokens = []
        i = 0

        while i < len(tokens):
            word, ccg, class_id, pos_seq = tokens[i]

            # NP/NP + NP → NP
            if ccg == "NP/NP" and i + 1 < len(tokens):
                next_word, next_ccg, next_class, next_pos = tokens[i+1]

                if next_ccg == "NP":
                    merged_word = word + next_word
                    merged_pos = pos_seq + next_pos

                    # ★ ログを保存
                    log_entries.append((
                        act_id, lang, step_no,
                        ccg, word,
                        next_ccg, next_word,
                        "NP", merged_word
                    ))
                    step_no += 1

                    new_tokens.append((merged_word, "NP", 301, merged_pos))
                    i += 2
                    changed = True
                    continue

            new_tokens.append(tokens[i])
            i += 1

        tokens = new_tokens

    # ★ DB にログを一括保存
    cur.executemany("""
        INSERT INTO ccg_log_tbl(
            act_id, lang, step_no,
            left_cat, left_word,
            right_cat, right_word,
            result_cat, result_word
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, log_entries)

    db.commit()

    return tokens

pos1_re = re.compile(r"(,|[#A-Z][A-Z_]+)")
pos2_re = re.compile(r"([#A-Z][A-Z_]+)")

def cnv_poslist(pos_seq):

    pos1_m = pos1_re.findall(pos_seq)
    pos1_m = ['SP' if x == ',' else x for x in pos1_m]
    pos1_m = tuple([x for x in pos1_m if not x.startswith('#')])
    pos2_m = tuple(pos2_re.findall(pos_seq))

    #print(pos_seq, pos1_m, pos2_m)
    # pos_seq は ('nn','nn') のような文字列なので eval でタプル化
    if pos_seq.startswith('(') :
        pos = pos2_m
    elif len(pos1_m) > 0:
        pos = pos1_m
    else:
        pos = pos_seq
    #print(pos)
  
    return pos

def load_tokens_from_box_tbl(db, act_id, lang):
    cur = db.cursor()

    cur.execute("""
        SELECT content, ccg, class_id, box_type
        FROM box_tbl
        WHERE act_id=? AND lang=?
        ORDER BY start_id
    """, (act_id, lang))

    rows = cur.fetchall()

    pos1_re = re.compile(r"(,|[#A-Z][A-Z_]+)")
    pos2_re = re.compile(r"([#A-Z][A-Z_]+)")

    tokens = []
    for content, ccg, class_id, pos_seq in rows:
        pos = cnv_poslist(pos_seq)
        print(pos)

        tokens.append((content, ccg, class_id, pos))

    return tokens

def save_ccg_tree(db, act_id, lang, nodes):
    cur = db.cursor()

    node_counter = 1

    def save_node(node, parent_id=None):
        nonlocal node_counter

        my_id = node_counter
        node_counter += 1

        cur.execute("""
            INSERT INTO ccg_tree_tbl(
                act_id, lang, node_id, parent_id,
                label, word, start_id, end_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            act_id, lang, my_id, parent_id,
            node["label"], node["word"],
            node["start"], node["end"]
        ))

        # 子ノードを保存
        for child in node.get("children", []):
            save_node(child, my_id)

    # 複数の木（forest）に対応
    for root in nodes:
        save_node(root)

    db.commit()

"""
# 実行例
assign_ccg_for_act(db, act_id=1, lang=1)

# 確認
show_ccg_skeleton(db, 1, 1)
"""

conn = sqlite3.connect("db/ccgDB.sqlite")

tokens = load_tokens_from_box_tbl(conn, act_id=1, lang=2)
nodes = apply_ccg_for_act(conn, 1, 2)
trees = build_ccg_tree(nodes)
save_ccg_tree(conn, 1, 2, trees)
