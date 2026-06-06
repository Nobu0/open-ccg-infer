
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

def assign_ccg_for_act(db, act_id, lang=1):
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

def merge_np_sequence(ccg_seq):
    merged = []
    buffer_words = []

    for word, ccg in ccg_seq:
        # 名詞（N）だけ統合対象
        if ccg == 'N':
            buffer_words.append(word)
        else:
            # N の連続が終わったらまとめて NP にする
            if buffer_words:
                merged.append(("".join(buffer_words), "NP"))
                buffer_words = []
            merged.append((word, ccg))

    # 最後に残った N をまとめる
    if buffer_words:
        merged.append(("".join(buffer_words), "NP"))

    return merged
"""
def merge_np_sequence(ccg_seq):
    merged = []
    buffer_words = []

    for word, ccg in ccg_seq:
        if ccg == 'NP':
            buffer_words.append(word)
        else:
            if buffer_words:
                merged.append(("".join(buffer_words), "NP"))
                buffer_words = []
            merged.append((word, ccg))

    if buffer_words:
        merged.append(("".join(buffer_words), "NP"))

    return merged
"""

def apply_ccg(seq):
    """
    seq: [(word, ccg), ...]
    """
    changed = True
    while changed:
        changed = False
        new_seq = []
        i = 0
        while i < len(seq):
            if i < len(seq)-1:
                left = seq[i][1]
                right = seq[i+1][1]

                # 前向き適用 X/Y  Y → X
                if '/' in left:
                    X, Y = left.split('/', 1)
                    if right == Y:
                        new_seq.append((seq[i][0] + ' ' + seq[i+1][0], X))
                        i += 2
                        changed = True
                        continue

                # 後ろ向き適用 Y  X\Y → X
                if '\\' in right:
                    X, Y = right.split('\\', 1)
                    if seq[i][1] == Y:
                        new_seq.append((seq[i][0] + ' ' + seq[i+1][0], X))
                        i += 2
                        changed = True
                        continue

            new_seq.append(seq[i])
            i += 1

        seq = new_seq

    return seq


db = "db/ccgDB.sqlite"
# 実行例
assign_ccg_for_act(db, act_id=1, lang=1)

# 確認
show_ccg_skeleton(db, 1, 1)
