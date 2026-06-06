
import sqlite3

def ccg_for_verb(pos, word):
    # 他動詞（目的語を1つ取る）
    # 法令文の「…を 〜する」はほぼこれ
    if pos.startswith('v'):
        return '(S\\NP)/NP'

    # 自動詞（目的語を取らない）
    # 必要なら辞書で例外処理
    if pos in {'vi', 'vz'}:
        return 'S\\NP'

    # デフォルト（動詞以外）
    return None

def ccg_for_case_particle(word):
        # 代表的な格助詞だけ例示
        if word == 'を':
            return '(S\\NP)/NP'      # 他動詞の目的語
        if word == 'に':
            return '((S\\NP)/NP)_ni' # に格
        if word == 'で':
            return '((S\\NP)/NP)_de'
        if word == 'から':
            return '((S\\NP)/NP)_kara'
        if word == 'まで':
            return '((S\\NP)/NP)_made'
        if word == 'と':
            return '((S\\NP)/NP)_to'
        if word == 'へ':
            return '((S\\NP)/NP)_e'
        if word == 'の':
            return '((S\\NP)/NP)_case'

        # その他の格助詞
        return '((S\\NP)/NP)_case'
    

def ccg_for_token(pos, word):
    # まず格助詞（格）を優先
    if pos == '格':
        # 代表的な格助詞だけ例示
        if word == 'を':
            return '(S\\NP)/NP'      # 他動詞の目的語
        if word == 'に':
            return '((S\\NP)/NP)_ni' # に格
        if word == 'で':
            return '((S\\NP)/NP)_de'
        if word == 'から':
            return '((S\\NP)/NP)_kara'
        if word == 'まで':
            return '((S\\NP)/NP)_made'
        if word == 'と':
            return '((S\\NP)/NP)_to'
        if word == 'へ':
            return '((S\\NP)/NP)_e'
        # その他の格助詞
        return '((S\\NP)/NP)_case'

    # 接続詞
    if pos == 'cc':
        return 'CONJ'

    # 名詞句内部の名詞（BOX 外で単独 NP にしたい場合に使うなら）
    if pos.startswith('nn'):
        return 'N'

    # 動詞（タグ体系に合わせて調整）
    if pos.startswith('v'):
        return 'S\\NP'

    # 形容詞・連体修飾など（必要に応じて拡張）
    if pos.startswith('adj'):
        return 'ADJ'

    # デフォルト
    return 'X'

def assign_ccg_token(pos, word, is_np):

    # BOX 内でも「名詞」だけ NP にする
    if is_np and pos.startswith('nn'):
        return 'NP'

    # 格助詞「の」
    if word == 'の':
        return '((S\\NP)/NP)_case'

    # 格助詞
    if pos == '格':
        return ccg_for_case_particle(word)

    # 動詞
    if pos.startswith('v'):
        return ccg_for_verb(pos, word)

    # 名詞
    if pos.startswith('nn'):
        #print(f"{word} nn -> N")
        return 'N'

    # 接続詞
    if pos == 'cc':
        return 'CONJ'

    return 'X'

def is_np_box(s, e, pos_line):
    poses = [pos for (_, pos, _) in pos_line[s:e+1]]

    # 節や動詞句を除外
    if any(p.startswith('v') for p in poses):
        return False

    # 名詞句の基本条件
    if poses[0].startswith('nn') and poses[-1].startswith('nn'):
        return True

    return False

def xxxxassign_ccg_for_act(db, act_id, lang=1):
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # 1. pos_tbl を取得（act_id＋lang 指定）
    cur.execute("""
        SELECT src_id, pos, word
        FROM pos_tbl
        WHERE act_id = ?
          AND lang = ?
          AND line_num < 3      
        ORDER BY src_id
    """, (act_id, lang))
    pos_line = cur.fetchall()  # [(src_id, pos, word), ...]

    # 2. NP BOX を取得（class_id=100 を NP とみなす）
    cur.execute("""
        SELECT start_id, end_id
        FROM box_tbl
        WHERE act_id = ?
          AND lang = ?
          AND class_id = 100
        ORDER BY start_id, end_id
    """, (act_id, lang))
    boxes = cur.fetchall()  # [(start_id, end_id), ...]
    np_boxes = [(s, e) for (s, e) in boxes if is_np_box(s, e, pos_line)]

    # 3. src_id → index マップ
    idx_of = {src_id: i for i, (src_id, pos, word) in enumerate(pos_line)}

    # boxes は (start, end) のリスト
    # これを最大区間だけにする
    max_boxes = []

    boxes_sorted = sorted(np_boxes, key=lambda x: (-(x[1]-x[0]), x[0]))

    max_np_boxes = []
    for s, e in boxes_sorted:
        if any(s >= ms and e <= me for ms, me in max_np_boxes):
            continue
        print(f"max_boxes append s={s}, e={e}")
        max_np_boxes.append((s, e))
    
    mark_np = [0] * len(pos_line)
    """
    for s, e in max_boxes:
        print(f"max_box s={s}, e={e}")
        for tid in range(s, e + 1):
            if tid in idx_of:
                mark_np[idx_of[tid]] = 1
    """            
    for s, e in max_boxes:
            for tid in range(s, e+1):
                if tid in idx_of:
                    mark_np[idx_of[tid]] = 1

    """
    # 4. NP 範囲マーキング
    mark_np = [0] * len(pos_line)
    for s, e in boxes:
      print("BOX:", s, e, "→", [w for (_,_,w) in pos_line[idx_of[s]:idx_of[e]+1]])
      for tid in range(s, e + 1):
            if tid in idx_of:
                mark_np[idx_of[tid]] = 1
    """
    # 1. pos_tbl 読み込み
    # 2. NP BOX 読み込み
    # 3. mark_np 作成

    # 4. CCG カテゴリ付与
    ccg_seq = []
    for i, (src_id, pos, word) in enumerate(pos_line):
        is_np = (mark_np[i] == 1)
        print("IN:", word, pos, is_np)
        ccg = assign_ccg_token(pos, word, is_np)
        print("OUT:", word, pos, is_np, "->", ccg)
        ccg_seq.append((word, ccg))   # ← word も残す
    print("Before merge:", ccg_seq[:20])

    # 5. ★ここで NP 統合を適用する
    ccg_seq = merge_np_sequence(ccg_seq[:20])
    print("After merge:", ccg_seq)

    # 6. 結合規則（FA/BA）を適用
    ccg_seq = apply_ccg(ccg_seq[:20])
    #print("After apply:", ccg_seq)

    # 6. 必要なら box_tbl や別テーブルに保存する
    # ここでは例として、box_tbl の ccg カラムに NP を書くのではなく、
    # token 単位の CCG を別テーブルに保存する形を示す

    cur.execute("DROP TABLE IF EXISTS ccg_token_tbl;")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ccg_token_tbl (
            src_id INTEGER, --PRIMARY KEY,
            act_id INTEGER,
            lang   INTEGER,
            ccg    TEXT,
            updt   DATETIME DEFAULT (DATETIME('now','localtime')),
            PRIMARY KEY (src_id, act_id)
        )
    """)

    print("INSERT:", src_id, type(src_id), act_id, type(act_id), lang, type(lang), ccg, type(ccg))

    for src_id, ccg in ccg_seq:
        cur.execute("""
            INSERT OR REPLACE INTO ccg_token_tbl (src_id, act_id, lang, ccg)
            VALUES (?, ?, ?, ?)
        """, (src_id, act_id, lang, ccg))

    conn.commit()
    conn.close()


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

def xxxbuild_ccg_tree(tokens):
    """
    tokens: [(word, ccg, class_id, pos_seq), ...]
    """

    # トークンを木ノードに変換
    nodes = [
        {"label": ccg, "word": word, "children": []}
        for (word, ccg, class_id, pos_seq) in tokens
    ]

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
                    # 結合
                    merged = {
                        "label": "NP",
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

"""
# 実行例
assign_ccg_for_act(db, act_id=1, lang=1)

# 確認
show_ccg_skeleton(db, 1, 1)
"""

conn = sqlite3.connect("db/ccgDB.sqlite")

#nodes = apply_ccg_for_act(conn, act_id=1, lang=1)


#nodes = build_ccg_tree(nodes)

#for n in nodes:
#    print(n["label"], n["word"], n["start"], n["end"])

#cur = conn.cursor()

# 1. BOX を start_id 順に取得
#cur.execute("""
#    SELECT content, ccg, class_id, box_type  --, start_id, end_id
#    FROM box_tbl
#    WHERE act_id=? AND lang=?
#    ORDER BY start_id
#    LIMIT 30        
#""", (1, 1))

#rows = cur.fetchall()

#tokens, log = apply_ccg_visualize(rows)

#print("=== APPLY CCG LOG ===")
#for line in log:
#    print(line)

#print("\n=== RESULT TOKENS ===")
#for w, c, cid, pos in tokens:
#    print(c, w)

# 1. box_tbl から tokens を取得
#tokens = load_tokens_from_box_tbl(conn, act_id=1, lang=1)

# 2. apply_ccg + ログ保存
#result_tokens = apply_ccg_and_save_log(conn, 1, 1, tokens)

tokens = load_tokens_from_box_tbl(conn, act_id=1, lang=1)
nodes = apply_ccg_for_act(conn, 1, 1)
trees = build_ccg_tree(nodes)
save_ccg_tree(conn, 1, 1, trees)
