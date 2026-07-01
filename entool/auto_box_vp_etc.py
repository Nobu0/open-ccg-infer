import sqlite3
from collections import defaultdict
import sys
import time
import ast

cand = []

PAT_CLASS = {
    101: {'typ':'#ADDR_ART', 'nam':'条（Article）'},
    102: {'typ':'#ADDR_PAR', 'nam':'項（Paragraph）'},
    103: {'typ':'#ADDR_NUM', 'nam':'号（Item Number）'},
    104: {'typ':'#ADDR_PAT', 'nam':'編（Part）'},
    105: {'typ':'#ADDR_CHA', 'nam':'章（Chapter）'},
    106: {'typ':'#ADDR_SEC', 'nam':'節（Section）'},
    107: {'typ':'#ADDR_SUB', 'nam':'款（Subsection）'},
    108: {'typ':'#ADDR_DIV', 'nam':'目（Division）'},

    201: {'typ':'#FIXED_PP',  'nam':'英語の固定前置詞句'},
    202: {'typ':'#FIXED_INF', 'nam':'英語の不定詞句'},

    301: {'typ':'', 'nam':"名詞句 (SIMPLE)"},
    302: {'typ':'', 'nam':"名詞句（REL）"},
    303: {'typ':'', 'nam':"アドレスを含む名詞句、数詞を含む(ADDR)"},
    304: {'typ':'', 'nam':"法令での名詞句等(OTHER)"},
    305: {'typ':'', 'nam':"その他の名詞句等(REFER)"},

    401: {'typ':'#CCG_LEFT',  'nam':'CCG 左結合（A/B + B → A）'},
    402: {'typ':'#CCG_RIGHT', 'nam':'CCG 右結合（B + B\\A → A）'},
    403: {'typ':'#VP',        'nam':'動詞句（Verb Phrase）'},

    501: {'typ':'#PP',     'nam':'前置詞句（英語）'},
    502: {'typ':'#ADV',    'nam':'副詞句'},
    503: {'typ':'#CLAUSE', 'nam':'節（S/NP, S\\NP など）'},
}

def process_pos_rows(cur, act, lang):
    # pos_tbl から行を取得
    cur.execute("""
        SELECT src_id, line_num, pos, word
        FROM pos_tbl
        WHERE act_id = ? AND lang = ?
        ORDER BY src_id
    """, (act,lang,))
    rows = cur.fetchall()

    # pos_seq / txt_seq / id_seq を作成
    pos_seq = [r[2] for r in rows]
    txt_seq = [r[3] for r in rows]
    id_seq  = [r[0] for r in rows]
    src = list(zip(pos_seq, txt_seq, id_seq))
    # BOX 抽出
    boxes = validate_Ngrams(src, cand)

    # insert_buffer を作成
    insert_buffer = []
    for class_id, pseq, tseq, ids in boxes:
        if len(ids) < 3:
            continue
        start_id = ids[0]
        end_id   = ids[-1]
        content  = " ".join(tseq)
        msg = PAT_CLASS[class_id]
        addm = ""
        if len(msg['typ'])> 0:
            addm = f" {msg['typ']}"
        type = " ".join(pseq)  # 300番台は純粋な品詞列、他は後でマーク付与
        box_type = f"{type}{addm}"

        insert_buffer.append((
            act,          # act_id
            lang,            # lang（英語=1）
            start_id,
            end_id,
            content,
            class_id,
            box_type
        ))

    return insert_buffer


def batch_box(conn, act_id=None, lang=2, batch_size=1000):

    cur = conn.cursor()

     # ----------------------------------------
    # 2. 対象 act_id の一覧を取得
    # ----------------------------------------
    if act_id is None:
        #cur.execute("SELECT DISTINCT act_id FROM pos_tbl WHERE act_id > 598 ORDER BY act_id")
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
        act_box_count = 0
        act_width_sum = 0

        insert_buffer = process_pos_rows(cur, act, lang)

        # BOX 数
        act_box_count += len(insert_buffer)

        # 幅の合計
        for row in insert_buffer:
            start_id = row[2]
            end_id   = row[3]
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
        end_time = time.perf_counter()
        # 所要時間の計算（秒）
        elapsed_time = end_time - start_time
        print(f"所要時間: {elapsed_time:.4f} 秒: {total_box} {total_width}")

    return total_box, total_width


def batch__history(conn, total_box, total_width=0, act_id=None, lang=2, name="BOX batch", desc="pos_box_tbl patterns"):
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

def loader(file, buf):
    # ファイルを読み込みモード('r')で開く
    with open(file, "r", encoding="utf-8") as file:
        for line in file:
            # 行末の改行コード等を除去
            line = line.strip()
            # 空行でなければ復元処理を実行
            if line.startswith("("):
                # 文字列をPythonのオブジェクト（リスト）に変換
                data_list = ast.literal_eval(line)
                buf.append(data_list)

def main_box(conn):

  # sys.argvには、実行時の引数が「文字列のリスト」として格納されます
  #args = sys.argv

  #print(f"実行ファイル名: {args[0]}")
      
  total_box,total_width = batch_box(
      conn,
      act_id=None,          # 全法令
      lang=2               # 英語
  )
  print(total_width)

  batch__history(conn,
      total_box,
      total_width,
      act_id=None,
      lang=2,
      name="VP、副詞句、前置詞句、WH節",
      desc="NX-gram(4)とに基づく句 BOX 化"
      )


def group_candidates_by_length(candidates):
    groups = defaultdict(set)
    for cand in candidates:
        groups[len(cand)].add(tuple(cand))
    return groups

#preps = {"in", "on", "with", "by", "for", "under", "over", "to", "of"}

def get_class_id(g):
    # FIXED_PP (201)
    if g[0] in {'IN'}: # PP 
        return 501
    if g[0] in {'RB'}: # 副詞句ADV
        return 502
    if g[0].startswith('W'): #W系CLAUSE
        return 503
    for pos in g:
        if pos.startswith("V"):
            return 403
    return None

##################################################
# 句を範囲を決定する関数
##################################################
def is_main_verb(pos, txt):
    """主節動詞の開始判定"""
    # MD + VB, VB*, BE/HAVE + VBN/VBG などをまとめて扱う
    if pos in ("VB", "VBD", "VBP", "VBZ"):
        return True
    if pos == "MD":
        return True
    if pos in ("VBN", "VBG") and txt not in ("prescribed", "provided", "given", "granted"):
        # provided/prescribed は後置修飾なので除外
        return True
    return False


def is_relation_clause_start(tokens, i):
    """ , which / , who / , where / , when / , that の判定 """
    if tokens[i][1] != ",":
        return False
    if i+1 >= len(tokens):
        return False

    pos, txt = tokens[i+1]

    # 非制限用法の関係節
    if pos in ("WDT", "WP", "WRB"):
        return True
    if txt.lower() == "that":
        return True

    return False


def is_condition_clause_start(tokens, i):
    """ provided, however, that / if / unless / when / where """
    txt = tokens[i][1].lower()

    if txt == "provided":
        # provided, however, that
        return True
    if txt in ("if", "unless", "when", "where"):
        return True

    return False


def is_np_continuation(pos, txt):
    """NP 継続条件（簡略版）"""
    if pos in ("NN", "NNS", "NNP", "NNPS", "DT", "JJ", "JJR", "JJS", "RB", "CD", "PRP$", "POS"):
        return True

    # PP の開始
    if pos == "IN":
        return True

    # 後置修飾（provided/prescribed/given/granted）
    if pos in ("VBN", "VBG") and txt.lower() in ("prescribed", "provided", "given", "granted"):
        return True

    # etc. は NP 内部
    if txt.lower() == "etc.":
        return True

    return False


def extract_np(tokens):
    i = 0
    L = len(tokens)

    while i < L:
        pos, txt = tokens[i]

        # --- 強制終端（法令文専用） ---
        if txt.lower() in ("shall", "may", "must", "can", "will", "should"):
            break

        # --- 通常の終端条件 ---
        if is_main_verb(pos, txt):
            break
        if txt in (".", ";"):
            break
        if is_relation_clause_start(tokens, i):
            break
        if is_condition_clause_start(tokens, i):
            break

        # --- IN の直後の DT/JJ/NN は PP 継続 ---
        if i > 0:
            prev_pos, prev_txt = tokens[i-1]
            if prev_pos == "IN" and pos in ("DT", "JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS"):
                i += 1
                continue

        # --- 単独継続条件 ---
        if is_np_continuation(pos, txt):
            i += 1
            continue

        break

    return tokens[:i]

def find_np_start(tokens, start_i, end_i, dbg=0):
    i = start_i
    lng = len(tokens)

    while i > (start_i - end_i) and i < lng:
        pos, txt = tokens[i]
        if dbg == 1:
            print("i=",i,pos,txt)
        # --- ここで止める条件 ---
        # IN の前には遡らない（NP は IN の直後から始まる）
        # 主節動詞の前には遡らない
        if pos in ("VB", "VBD", "VBP", "VBZ", "MD", "IN", "TO", "CC"):
            break

        # --- 遡ってよい条件 ---
        if pos in ("DT", "JJ", "JJR", "JJS", "RB", "CD",
                    "NN", "NNS", "NNP", "NNPS", "PRP$", "POS"):
            i -= 1
            continue

        break

    return i


def extract_WH_clause(sta, tokens):
    i = 0
    L = len(tokens)

    while i < L:
        pos, txt = tokens[i]

        # 終端条件
        if txt in (",", ";", ".", "(", ")"):
            break
        if pos in ("VB", "VBD", "VBP", "VBZ", "MD"):
            break
        if txt.lower() in ("and", "or"):
            break
        if txt.lower() == "provided":
            break

        i += 1

    return sta + i

def text_trim(txt):                   
    bad_tail = {"the", "a", "an", "(", ":", ")"}
    while txt and txt[-1].lower() in bad_tail:
        txt = txt[:-1]
    return txt

def validate_Ngrams(src, cand_by_len):
    result = []

    tokens = [r[0] for r in src]
    toktxt = [r[1] for r in src]

    toks = list(zip(tokens, toktxt))
    L = len(tokens)
 
    for ngm, candset in cand_by_len.items():
        if L < ngm:
            continue

        # i=0 から L-ngm まで統一処理
        for i in range(0, L - ngm + 1):

            window = tuple(tokens[i:i+ngm])
            
            class_id = get_class_id(window)
            if window in candset:

                tsrc = toktxt[i:i+ngm+10]
                #counter[window] += 1

                if class_id == 503: # WH句
                    #tmptoks = toks[i:i+ngm] + 
                    ku_end = extract_WH_clause(i+ngm, toks[i+ngm:])
                    txt = text_trim([txt for (_, txt) in toks[i:ku_end]])  # NP のテキスト
                    if ku_end - i != len(txt):
                        ku_end = i+len(txt)
                else:    
                    np_start = find_np_start(toks, i+ngm, ngm)
                    np_slice = toks[np_start:]          # ここからが「NP 候補」
                    np_tokens = extract_np(np_slice)      # 終端関数で NP 部分だけ切り出す
                    ku_end = np_start + len(np_tokens)
                    txt = text_trim([txt for (_, txt) in toks[i:ku_end]])  # NP のテキスト
                    if ku_end - i != len(txt):
                        ku_end = i+len(txt)

                result.append([
                    class_id,
                    [r[0] for r in src[i:ku_end]],
                    [r[1] for r in src[i:ku_end]],
                    [r[2] for r in src[i:ku_end]]
                ])

    return result


###############################################################
# 品詞パターンを読み込んで、トークンリストを解析しDBへBOX登録する。
###############################################################
# 開始時間の取得
start_time = time.perf_counter()
args = sys.argv

print(f"実行ファイル名: {args[0]}")
print(f"品詞ファイル名: {args[1]}")

buf = []
file = args[1]

loader(file, buf)
cand = group_candidates_by_length(buf)

for l in cand:
  print(l)
#exit()

conn = sqlite3.connect("db/ccgDB.sqlite")

main_box(conn)

end_time = time.perf_counter()
# 所要時間の計算（秒）
elapsed_time = end_time - start_time
print(f"所要時間: {elapsed_time:.4f} 秒")
