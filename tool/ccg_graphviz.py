import sqlite3


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
        pos = eval(pos_seq) if isinstance(pos_seq, str) else pos_seq
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

def load_tokens_from_box_tbl(db, act_id, lang):
    cur = db.cursor()

    cur.execute("""
        SELECT content, ccg, class_id, box_type
        FROM box_tbl
        WHERE act_id=? AND lang=?
        ORDER BY start_id
    """, (act_id, lang))

    rows = cur.fetchall()

    tokens = []
    for content, ccg, class_id, pos_seq in rows:
        # pos_seq は ('nn','nn') のような文字列なので eval でタプル化
        if isinstance(pos_seq, str):
            pos = eval(pos_seq)
        else:
            pos = pos_seq

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



def ccg_forest_to_dot(forest, graph_name="CCG"):
    lines = []
    lines.append(f'digraph {graph_name} {{')
    #lines.append('  rankdir=LR;')
    lines.append('  node [shape=box, fontname="IPAGothic"];')

    node_id_counter = 1
    id_map = {}

    def emit_node(node):
        nonlocal node_id_counter
        my_id = f"n{node_id_counter}"
        node_id_counter += 1
        id_map[id(node)] = my_id

        label = f"{node['label']}\\n{node['word']}"
        lines.append(f'  {my_id} [label="{label}"];')

        for child in node.get("children", []):
            child_id = emit_node(child)
            lines.append(f'  {my_id} -> {child_id};')

        return my_id

    for root in forest:
        emit_node(root)

    lines.append('}')
    return "\n".join(lines)

from graphviz import Source

def save_png_from_dot(dot_text, filename="ccg_tree"):
    src = Source(dot_text)
    src.format = "png"
    src.render(filename, cleanup=True)


conn = sqlite3.connect("db/ccgDB.sqlite")

tokens = load_tokens_from_box_tbl(conn, act_id=1, lang=1)
nodes = apply_ccg_for_act(conn, 1, 1)
trees = build_ccg_tree(nodes)
save_ccg_tree(conn, 1, 1, trees)

dot = ccg_forest_to_dot(trees)
with open("ccg_tree.dot", "w", encoding="utf-8") as f:
    f.write(dot)

save_png_from_dot("ccg_tree.dot", filename="ccg_tree")
