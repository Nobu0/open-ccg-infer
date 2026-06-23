import ast
import sys
import os
import re
from collections import Counter, defaultdict

counter = Counter()
cotBox = Counter()

# ノイズ語
NOISE = {'(', ')', ',', '.', 'sp', ';', ':'}
CODE = {'CD', 'DT', 'NNP'}
NOISE = {'(', ')', ',', '.', 'sp','-RRB-','-LRB-',"''",'``',':'}
linesH = []
linesT = []
textBuf = []
linesTH = []

box_map = {}

PATTERNS = {
    # 英語
    ('JJ', 'TO', 'DT', 'NNS', 'IN'):1,
    ('JJ','TO','NNP','CD'):1,
    ('NN','NN','JJ','TO'):1,
    ('JJ','NNS','IN','DT','NN'):1, # add
    ('VBZ', 'VBN', 'TO', 'VB', 'VBN', 'VBN'):1, #add
    ('VBN', 'TO', 'VB', 'VBN', 'VBN', 'IN'):1, #add
    ('VB', 'VBN', 'TO', 'VB', 'VBN', 'VBN'):1, #add
    ('VBZ', 'VBN', 'TO', 'VB', 'VBN', 'IN'):1, #add
    ('VB', 'VBN', 'TO', 'VB', 'VBN', 'IN'):1, #add
    ('VBZ', 'VBN', 'TO', 'VB', 'VBN', 'IN'):1, #add
    ('MD', 'VB', 'DT', 'VBG', 'NNS', 'IN'):1, #add
    ('IN','JJ','NNP','NNPS'):1, # add
    ('MD','VB','VBN','TO'):1, # add
    ('MD','VB','VBN','IN'):1, # add
    ('MD','VB','TO','IN'):1, # add
    ('MD','VBN','TO','IN'):1, # add
    ('MD','VB','VBN','TO','IN'):1, # add
    ('VBZ', 'VBN', 'TO', 'VB'):1, #add
    ('VB', 'VBN', 'TO', 'VB', 'VBN', 'IN'):1, #add
    ('VBP', 'VBN', 'TO', 'VB', 'VBN', 'IN'):1, #add
    ('VBZ', 'VBN', 'TO', 'VB', 'VBN', 'IN'):1, #add
    ('VB', 'VBN', 'TO', 'VB', 'VBN'):1, #add
    ('VBZ', 'TO', 'VB', 'CC', 'VB'):1, #add
    ('MD', 'VB', 'VBN', 'CC', 'VBN', 'IN'):1, #add
    ('MD', 'VB', 'VBN', 'RB'):1, #add
    ('VBZ', 'VBN', 'TO', 'VB', 'VBN'):1, #add
    ('VBZ', 'RB', 'VBN', 'TO', 'VB'):1, #add
    ('VBZ', 'RB', 'JJ', 'TO', 'VB'):1, #add
    ('VBN', 'RB', 'IN'):1, #add
    ('VBN', 'RB', 'TO'):1, #add
    ('VBD', 'RB', 'IN'):1, #add
    ('VBZ', 'RB', 'VB'):1, #add
    ('VBZ', 'RB', 'VBN'):1, #add
    ('VBP', 'RB','RB'):1, #add
    ('VBD', 'RB'):1, #add
    ('VBP', 'RB'):1, #add
    ('IN', 'RB', 'JJR'):1, #add
    ('VB', 'VBN', 'TO', 'VB'):1, #add
    ('MD','VBG','TO','IN'):1, # add
    ('IN', 'RB', 'JJR', 'IN'):1, #add
    ('IN', 'NNP', 'CD', 'IN', 'DT', 'NNP'):1, #add
    ('IN', 'NNS', 'WRB', 'EX', 'VBZ'):1, #add
    ('IN', 'WDT', 'CD', 'NNS', 'VBP', 'VBN', 'IN'):1, #add
    ('IN', 'WDT', 'CD', 'NNS', 'VBP', 'VBN', 'IN'):1, #add
    ('IN', 'NNS', 'WRB', 'DT', 'NNS', 'IN'):1, #add
    ('WRB', 'DT', 'NNP', 'NNP', 'VBZ', 'VBN'):1, #add
    ('WRB', 'EX', 'VBP', 'CD', 'CC', 'JJR'):1, #add
    ('WRB', 'DT', 'NNP', 'NNP', 'VBZ'):1, #add
    ('WDT', 'VBP', 'VBN', 'IN', 'NNS', 'IN'):1, #add
    ('IN', 'WP', 'CD', 'NNS', 'VBP', 'RB', 'VBN'):1, #add
    ('WRB', 'CD', 'NNS', 'VBP', 'VBN', 'IN'):1, #add
    ('WDT', 'VBZ', 'VBN', 'IN', 'NNS', 'IN'):1, #add
    ('WDT', 'VBP', 'VBN', 'IN', 'NNS', 'IN'):1, #add
    ('WDT', 'VBP', 'TO', 'VB', 'VBN', 'IN'):1, #add
    ('WDT', 'VBP', 'VBN', 'TO', 'VB', 'VBN'):1, #add
    ('WRB', 'DT', 'NNP', 'IN', 'DT', 'NNP', 'NNP'):1, #add
    ('WRB', 'DT', 'NNP', 'IN', 'NNP', 'VBZ'):1, #add
    ('WRB', 'DT', 'NN', 'IN', 'NN', 'VBZ', 'VBN'):1, #add
    ('WP', 'VBZ', 'VBN', 'TO', 'VB', 'DT', 'NN', 'IN'):1, #add
    ('WRB', 'DT', 'NN', 'VBZ', 'VBN', 'VBN', 'IN'):1, #add
    ('WRB', 'VBG', 'DT', 'NN', 'IN', 'NN', 'IN'):1, #add
    ('WRB', 'DT', 'JJ', 'NN', 'NN', 'VBZ', 'VBN'):1, #add
    ('WRB', 'DT', 'VBN', 'NN', 'NN', 'VBZ'):1, #add
    ('IN', 'NNS', 'WRB', 'DT', 'NNS', 'IN'):1, #add
    ('WRB', 'DT', 'NNP', 'NNP', 'NNP', 'NNP', 'VBZ', 'VBN'):1, #add
    ('WDT', 'VBZ', 'VBN', 'DT', 'NN', 'IN', 'NN'):1, #add
    ('WDT', 'VBZ', 'VBN', 'IN', 'NN', 'IN'):1, #add
    ('WRB', 'DT', 'NN', 'VBZ', 'VBN', 'DT', 'NN', 'IN'):1, #add
    ('WP', 'VBZ', 'VBN', 'DT', 'NN', 'IN', 'NN', 'IN'):1, #add
    ('WRB', 'VBG', 'DT', 'NN', 'IN', 'NN', 'IN'):1, #add
    ('WRB', 'NN', 'VBZ', 'VBN', 'DT', 'NN', 'IN'):1, #add
    ('WRB', 'DT', 'NNP', 'NNP', 'VBZ', 'DT', 'NN'):1, #add
    ('WRB', 'DT', 'NNP', 'VBZ', 'VBN'):1, #add
    ('WRB', 'DT', 'JJ', 'NN', 'VBZ', 'VBN', 'DT', 'NN'):1, #add
    ('WRB', 'DT', 'NN', 'NN', 'VBZ', 'VBN'):1, #add
    ('WP', 'VBZ', 'TO', 'VB', 'DT', 'NN', 'IN', 'NN'):1, #add
    ('WDT', 'VBP', 'VBN', 'TO', 'VB', 'JJ'):1, #add
    ('WRB', 'DT', 'NN', 'NN', 'VBZ', 'VBN', 'IN'):1, #add
    ('WRB', 'DT', 'NNS', 'VBN', 'IN', 'NNP'):1, #add 
    ('WRB', 'DT', 'NNS', 'VBN', 'IN', 'NNP', 'CD'):1, #add
    ('IN', 'NNS', 'WRB', 'DT', 'JJ', 'NN', 'NN'):1, #add
    ('IN', 'PRP', 'VBZ', 'JJ', 'TO', 'VB'):1, #add
    ('WRB', 'DT', 'NNP', 'VBZ', 'VBN', 'DT', 'NN'):1, #add
    ('WDT', 'VBZ', 'DT', 'NNS', 'VBN', 'IN'):1, #add
    ('IN', 'NNS', 'WRB', 'DT', 'NN', 'VBN', 'IN'):1, #add
    ('WDT', 'VBZ', 'VBN', 'IN', 'NN', 'IN'):1, #add
    ('WRB', 'NN', 'VBZ', 'VBN', 'DT', 'NN', 'IN'):1,
    ('WRB', 'DT', 'NN', 'IN', 'NN', 'IN', 'NN'):1,
    ('WRB', 'DT', 'NN', 'VBZ', 'VBN', 'VBN', 'IN'):1,
    ('WRB', 'DT', 'NNP', 'NNP', 'VBZ'):1,
    ('WDT', 'VBP', 'VBN', 'IN', 'NNS', 'IN'):1,
    ('IN', 'NNS', 'WRB'):1, #add
    ('IN', 'WDT'):1, #add
    ('MD','RB','VB'):1, # add
    ('MD','VB','IN'):1, # add
    ('VB','TO','IN'):1, # add
    ('VBP','TO','IN'):1, # add
    ('VBZ','TO','IN'):1, # add
    ('VBD','TO','IN'):1, # add
    ('VBZ', 'TO', 'VB'):1, #add
    ('JJ','JJ','NN'):1, # add
    ('WRB', 'PRP', 'VBZ'):1, #add
    ('IN','WDT'):1, #add
    ('WP','VBZ'):1, #add
    ('IN','VBN','IN'):1,
    ('NNP','NNP','NNP'):1,
    ('NN','JJ','TO'):1,
    ('NN','JJ','IN'):1,
    ('IN','DT','NN'):1,
    ('TO','DT','NN'):1,
    ('NNP','CD'):1,
    ('DT','NN'):1,
    ('IN','DT'):1,
    ('TO','DT'):1,
    ('JJ','NN'):1,
    ('JJ','IN'):1,
    ('JJ','TO'):1,
}

PATTERN_INDEX = defaultdict(list)

def init_pattern():      
    for pat in PATTERNS.keys():
        first = pat[0]              # pat は tuple
        PATTERN_INDEX[first].append(pat)

    # 最長一致優先
    for first in PATTERN_INDEX:
        PATTERN_INDEX[first].sort(key=len, reverse=True)

def compress(tokens):
    i = 0
    result = []

    while i < len(tokens):
        first = tokens[i]
        matched = False

        # 先頭品詞が一致するパターンだけを見る
        for pat in PATTERN_INDEX.get(first, []):
            L = len(pat)
            # tokens[i:i+L] は list → tuple に変換して比較
            if tuple(tokens[i:i+L]) == pat:
                result.append("_".join(pat))
                i += L
                matched = True
                break

        if not matched:
            result.append(tokens[i])
            i += 1

    return result


def xxxxcompress(tokens, patterns=PATTERNS):
    """
    patterns: PATTERNS で品詞を結合
    """
    i = 0
    result = []

    while i < len(tokens):
        matched = False

        for pat, _ in patterns.items():
            L = len(pat)
            if tuple(tokens[i:i+L]) == pat:
                lab = "_".join(pat) 
                result.append(lab)
                i += L
                matched = True
                break

        if not matched:
            result.append(tokens[i])
            i += 1

    return result

def decompress_list(tokens, patterns=PATTERNS):
    buf = []
    for toks in tokens:
        lst = decompress(toks, patterns)
        buf.append(lst)
    return buf

def decompress(tokens, patterns=PATTERNS):
    # 結合を分解
    result = []
    for t in tokens:
        lst = t.split("_")
        result.extend(lst)

    return result


def append_box(key, tokens, src):
      sky = tuple(tokens)
      if key not in box_map:
        box_map[key] = {
              "count": 0,
              "examples": {},
              "pattern": None,   # 射パターンを後で入れる
          }
      box_map[key]["count"] += 1
      if sky not in box_map[key]["examples"]:
        box_map[key]["examples"][sky] = {
          "count": 0,
          "text": "",
          "src": ""
        }
      box_map[key]["examples"][sky]["count"] += 1  
      box_map[key]["examples"][sky]["text"] = tokens
      box_map[key]["examples"][sky]["src"] = src


def load_src(dir, no, mx=635):
    hno = no
    kno = no - 1
    lno = 2
    for i in range(1, mx):
        file_name = f"{dir}/src_{i}.txt"
        if not os.path.exists(file_name):
            continue
        # 形態素ファイルを開く
        ln = ""
        buf = [] 
        tmp = []
        with open(file_name, 'r', encoding='utf-8') as f:
            for line in f:
                #print(line)  
                line = line.replace('\t', ' ')
                line = line.replace('\u3000', ' ')  # 全角スペース
                line = line.strip()
                toks = line.split()
                if len(toks) <= max(hno, kno):
                    #print("列不足:", toks)
                    continue
                if toks[lno] != ln and ln != "":
                    #print(len(toks), tmp)        
                    linesTH.append(tmp)
                    tmp = []
                ln = toks[lno] 
                tmp.append((toks[hno], toks[kno])) 
        linesTH.append(tmp) 

def write_file(file, src):
    with open(file, "a", encoding="utf-8") as file:
      for tmp in src:
          file.write(f"{tmp}\n")
    
# 4-gram が有用かどうか判定
def is_useful_4gram(g):
    # ノイズを含むものは除外
    if any(tok in NOISE for tok in g):
        return False
    return True

def make_Ngram_candidates(grams, overlap, target_len):
    """
    grams: list of tuples (元の n-gram 群)
    overlap: 何語オーバーラップさせるか
    target_len: 作りたい n-gram の長さ
    """
    candidates = set()
    g_list = list(grams)
    base_len = len(g_list[0])  # 元の n-gram の長さ

    # 結合後の長さチェック
    if target_len != base_len * 2 - overlap:
        raise ValueError("target_len は base_len*2 - overlap と一致する必要があります")

    for a in g_list:
        for b in g_list:
            # a の後ろ overlap 語 と b の前 overlap 語 が一致するか
            if a[-overlap:] == b[:overlap]:
                # 結合：a の前半 + b の後半
                new_ngram = a + b[overlap:]
                candidates.add(new_ngram)

    return candidates

def sliding_windows(seq, n):
    for i in range(len(seq) - n + 1):
        yield i, seq[i:i+n]

##################################################
# 句を範囲を決定する関数軍
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


def extract_WH_clause(tokens):
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

    return tokens[:i]

def text_trim(txt):                   
    bad_tail = {"the", "a", "an", "(", ":", ")"}
    while txt and txt[-1].lower() in bad_tail:
        txt = txt[:-1]
    return txt

def validate_Ngrams(src, cand_by_len):
    counter = Counter()
    for toks in src:
        tokens = [pos for (pos,txt) in toks]
        toktxt = [txt for (pos,txt) in toks]
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
                    counter[window] += 1

                    if class_id == 503: # WH句
                        tmptoks = toks[i:i+ngm] + extract_WH_clause(toks[i+ngm:])
                        txt = text_trim([txt for (_, txt) in tmptoks])  # NP のテキスト
                    else:    
                        np_start = find_np_start(toks, i+ngm, ngm)
                        np_slice = toks[np_start:]          # ここからが「NP 候補」
                        np_tokens = extract_np(np_slice)      # 終端関数で NP 部分だけ切り出す
                        np_end = np_start + len(np_tokens)
                        txt = text_trim([txt for (_, txt) in toks[i:np_end]])  # NP のテキスト

                    append_box(
                        window,              # N-gram 自体
                        txt,
                        tsrc
                    )

    return counter

def detect_offset(tokens, i, ngm, window):
    """
    tokens: POS のリスト
    i: validate_Ngrams の window の開始位置
    ngm: N-gram 長
    window: 現在の window (tuple of POS)
    """
    # 文中の実際の N-gram
    actual = tuple(tokens[i:i+ngm])

    # window と文中の N-gram が一致していなければズレ
    if actual != window:
        return True, actual
    return False, actual

def validate_Ngrams_simple(src, cand_by_len):
    counter = Counter()
    for toks in src:
        tokens = [pos for (pos,txt) in toks]
        toktxt = [txt for (pos,txt) in toks]
        L = len(tokens)

        for ngm, candset in cand_by_len.items():
            if L < ngm:
                continue

            # 初期ウィンドウ
            window = tuple(tokens[:ngm])

            # i=0 から L-ngm まで統一処理
            for i in range(0, L - ngm + 1):

                # i>0 のときだけローリング更新
                if i > 0:
                    window = window[1:] + (tokens[i+ngm-1],)

                if window in candset:
                    append_box2(window, toktxt[i:i+ngm])
                    counter[window] += 1

    return counter


def ngrams(tokens, n=4):
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def make_ngrams(seq, n):
    return [tuple(seq[i:i+n]) for i in range(len(seq)-n+1)]

def nx_ngram(pos_seq, n=10, pat=PATTERNS):
    key = compress(pos_seq)  # cdhd+cd+nnt を合体
    return make_ngrams(key, n)            # 10-gram を取る

def ngram_freq(tokens, n=4, pat=PATTERNS):
    # tokens は 1行分のトークン列（リスト）
    counter.update(nx_ngram(tokens, n, pat))
    
def get_pattern(lines,pat):
    i = 0
    for cols in lines:      
        if len(cols) < 4:
          continue
        co = [pos for (pos,txt) in cols]
        ngram_freq(co, 4, pat)
        i += 1

def is_noise(gram):
    return any(tok in NOISE for tok in gram)

def is_code(gram):
    return any(tok in CODE for tok in gram)

def classify_ccg(tags):
    # NP/NP
    if tags[0] in {"IN", "TO"}:
        return "NP/NP"

    # NP\NP
    if tags[-1] in {"の"} or tags[0] in {"JJ", "WDT"}:
        return "NP\\NP"

    # S\NP
    if tags[-1] in {"VB", "VBN"}:
        return "S\\NP"

    # S/S
    if tags[0] == "IN" and tags[1] in {"VBG", "VBN"}:
        return "S/S"

    return "OTHER"

def loader(file, buf):
    # ファイルを読み込みモード('r')で開く
    with open(file, "r", encoding="utf-8") as file:
        for line in file:
            # 行末の改行コード等を除去
            line = line.strip()
            
            # 空行でなければ復元処理を実行
            if line:
                # 文字列をPythonのオブジェクト（リスト）に変換
                data_list = ast.literal_eval(line)
                buf.append(data_list)

def  box_hantei(tags):
    if tags[0] in {'MD',"RB","IN"}:
        return "Okay"
    
    if tags[0].startswith("VB"): 
        return "Okay"
    
    if tags[0].startswith("W"):
            return "Okay"

    return None



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

def extract_vp_boxes(pos_seq, token, existing_boxes):
    vp_boxes = []
    n = len(token)
    i = 0

    while i < n:
        word = token[i]
        pos = pos_seq[i]

        if is_vp_start(word, pos):
            start = i
            j = i + 1

            while j < n:
                w = token[j]
                p = pos_seq[j]
                if not is_vp_extend(w, p, token, pos_seq, j, existing_boxes):
                    break
                j += 1

            if j - start >= 2:
                vp_boxes.append((start, j-1))

            i = j
        else:
            i += 1

    return vp_boxes

def is_vp_start(word, pos):
    if pos == "MD":
        return True
    if pos in {"VB", "VBP", "VBZ", "VBD"}:
        return True
    if word.lower() in {"is", "are", "was", "were", "be", "been", "being"}:
        return True
    return False

def is_vp_extend(word, pos, token, pos_seq, j, existing_boxes):
    if pos in {"VB", "VBN", "VBG", "VBP", "VBZ"}:
        return True
    if pos == "TO":
        return True
    if pos == "IN" and next_is_np(token, pos_seq, j, existing_boxes):
        return True
    return False

# 品詞パターンの取得とトークンリストの最終形までを検証するツール
# DBへの実登録は行わない。
if __name__ == "__main__":
    args = sys.argv

    print(f"実行ファイル名: {args[0]}")
    print(f"第1引数: {args[1]}")

    NX_Gram = 6
    if args[1] == 4:
        NX_Gram = 4
    init_pattern()
    ####load_src("../act-monad/data/tsv/en1", 7)
    ####write_file("en_list.txt",linesTH)
    loader("en_list.txt",linesTH)
    #loader("en_list_test.txt",linesTH)
    print(f"data: text length={len(linesTH)}")
    #for tmp in linesTH:
    #    print(tmp)
    #print("POSをロード完了")
    get_pattern(linesTH,PATTERNS)
    #print("POSをNX-gram実行完了")

    MX = 5000
    START = 0
    # すでに抽出済みの 4-gram 頻度（例）
    # 実際にはあなたの counter.most_common() の結果を使う
    fourgram_freq = counter.most_common(MX)

    # 4-gram 部分だけ取り出す
    fourgrams = [g for (g, c) in fourgram_freq]

    # 有用な 4-gram のみ抽出
    useful_4grams = [g for g in fourgrams if is_useful_4gram(g)]

    # 4+4-2 で 6-gram 仮説生成
    #print("POSをNX-gramを合成")
    candidatesNX=[]
    if NX_Gram == 4:
      candidatesNX = decompress_list(useful_4grams)
    else:
      candidates6 = make_Ngram_candidates(useful_4grams,2,6)
      #candidates10 = make_Ngram_candidates(candidates6,2,10)
      #candidates18 = make_Ngram_candidates(candidates10,4,16)
      candidatesNX = decompress_list(candidates6)
    
    candidates = group_candidates_by_length(candidatesNX)
    #print("POSの合成を分解完了")
    #for tmp in candidates:
    #print(f"length= {len(candidates)}")

    # 生データで検定
    #file = "../act-monad/data/stxen.txt"
    validated = validate_Ngrams(linesTH, candidates)
    #print("POSのパターンでテキストを取り出し完了")

    i = 1
    p = -1
    cnt = 0
    for g, c in validated.most_common(MX):
        if box_hantei(g) == None:
            continue
        cls_id = get_class_id(g)
        if cls_id == None:
            continue
        print(g)
        i += 1
    
    exit()
    # 出現頻度順に表示
    i = 1
    p = -1
    cnt = 0
    for g, c in validated.most_common(MX):
        p += 1
        if p < START:
          continue
        if box_hantei(g) == None:
            continue
        cls_id = get_class_id(g)
        if cls_id == None:
            continue
        cnt += c
        print("-------------------------------------")
        print('###', g, c, cnt, i, len(g), cls_id)
        i += 1    
        cc = 0
        #for ex in sorted(box_map[g]["examples"].items(), key=lambda x: x[1], reverse=True):
        #sublist = box_map[g]["examples"]
        data = [box_map[g]["examples"][ky] for ky in box_map[g]["examples"]]
        #print(data)
        sorted_data = sorted(data, key=lambda x: x['count'], reverse=True)
        for item in sorted_data:
            #class_id = get_class_id(item["text"])
            if item["count"] < 2:
                break
            print(item["count"], item["text"], cls_id)
            #print("T:",item["count"], item["text"], cls_id)
            #print("S:",item["count"], item["src"], cls_id)
            if cc > 10:  break
            cc += 1

        #for info in sorted(sublist.itmes(), key=lambda x: x["count"], reverse=True):
        #    print(info)

      #if i > 20: break
      #i += 1    
