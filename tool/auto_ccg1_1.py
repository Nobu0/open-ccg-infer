import ast
import os
import re
from collections import Counter, defaultdict

counter = Counter()
cotBox = Counter()

# ノイズ語
NOISE = {'(', ')', ',', '.', 'sp'}
linesH = []
linesT = []
textBuf = []
linesTH = []

box_map = {}

PATTERNS = {
    # 日本語
    # 第XX号　等
    ('cdhd','cd','nnt'): ('ADDR', ['cdhd','cd','nnt']),
    ('nnp','cd','nnt'): ('ADDR', ['cdhd','cd','nnt']),
    ('nn', 'nn', 'nn', 'nn'): ('TAG92',['nn', 'nn', 'nn', 'nn']), 
    ('nn', 'nn', 'nn'): ('TAG93',['nn', 'nn', 'nn']), 
    ('nn', 'nn'): ('TAG94',['nn', 'nn']), 
    ('nns', 'nns', 'nns'): ('TAG95',['nns', 'nns', 'nns']), 
    ('nns', 'nns'): ('TAG96',['nns', 'nns']), 
    ('nn', 'nns', 'nnt'): ('TAG97',['nn', 'nns', 'nnt']), 
    ('nn', 'nn', 'nnt'): ('TAG103',['nn', 'nn', 'nnt']), 
    ('nn', 'nnt'): ('TAG104',['nn', 'nnt']), 
    ('nnp', 'nnt'): ('TAG98',['nnp', 'nnt']), 
    ('nnp', 'nn'): ('TAG99',['nnp', 'nn']), 
    # 受け た もの と みなす
    ('vb', '助動', 'nnh', '格', 'vb'):('DEEMED', ['vb', '助動', 'nnh', '格', 'vb']),  
    ('助動', '接', 'vbo', '助動'): ('MUST', ['助動', '接', 'vbo', '助動']),
    #('して','は','なら','ない'): ('PROHIBIT', ['して','は','なら','ない']),
    ('接', '係', 'vbo', '助動'): ('PROHIBIT', ['接', '係', 'vbo', '助動']),
    #('する','こと','が','できる'): ('ALLOW', ['する','こと','が','できる']),
    ('vb', 'nnh', '格', 'vb'): ('ALLOW', ['vb', 'nnh', '格', 'vb']),
    ('nn','nns','格','nns','vb','助動','nnh','格','vb','nnh'):
    ('ORDER_MUST',['nn','nns','格','nns','vb','助動','nnh','格','vb','nnh']),
    #('vb', 'さ'), ('vbt', 'れ'), ('接', 'て'), ('vbo', 'い'), ('助動', 'ない')
    ('vb', 'vbt', '接', 'vbo', '助動'): ('TAG1',['vb', 'vbt', '接', 'vbo', '助動']),
    #('vb', 'つとめ'), ('助動', 'なけれ'), ('接', 'ば'), ('vbo', 'なら'), ('助動', 'ない')
    ('vb', '助動', '接', 'vbo', '助動'): ('TAG2',['vb', '助動', '接', 'vbo', '助動']),
    #('vb', '要し'), ('助動', 'ない'), ('nnh', 'もの'), ('格', 'と'), ('vb', 'する')
    ('vb', '助動', 'nnh', '格', 'vb'): ('TAG3',['vb', '助動', 'nnh', '格', 'vb']),
    #('vb', '行う'), ('nnh', 'こと'), ('格', 'を'), ('vb', '妨げ'), ('助動', 'ない')
    ('vb', 'nnh', '格', 'vb', '助動'): ('TAG6',['vb', 'nnh', '格', 'vb', '助動']),
    #('nnjv', '必要'), ('格', 'が'), ('vb', 'ある')
    ('nnjv', '格', 'vb'): ('TAG5',['nnjv', '格', 'vb']),
    #('nnjv', '必要'), ('助動', 'な')
    ('nnjv', '助動'): ('TAG4',['nnjv', '助動']),
    ('vb', 'nnh', '格', '終', 'nn'): ('TAG90',['vb', 'nnh', '格', '終', 'nn']),
    ('vb', '助動', 'nnh'): ('TAG91',['vb', '助動', 'nnh']), 
    ('格', 'efl', 'nn'): ('TAG100',['格', 'efl', 'nn']),
    ('nnh', '格', 'vb', 'vbt', '助動'): ('TAG101',['nnh', '格', 'vb', 'vbt', '助動']),
    ('助動', '助動'): ('TAG102',['助動', '助動']),
    ('nns', 'vb', '助動', 'nn'): ('TAG201',['nns', 'vb', '助動', 'nn']),
    # 英語
    #('shall','be','deemed','to'): ('DEEMED', ['shall','be','deemed','to']),
    #('in','accordance','with'): ('INACC', ['in','accordance','with']),
}


def compress(tokens, patterns=PATTERNS):
    """
    tokens: ['cdhd','cd','nnt','nn','格', ...] など
    patterns: PATTERNS 辞書
    """
    i = 0
    result = []

    while i < len(tokens):
        matched = False

        for pat, (label, _) in patterns.items():
            L = len(pat)
            if tuple(tokens[i:i+L]) == pat:
                result.append(label)
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
    """
    tokens: ['ADDR','nn','格', ...] など
    """
    # ラベル → 元リスト の辞書を作る
    reverse = {label: original for (_, (label, original)) in patterns.items()}
    result = []
    for t in tokens:
        if t in reverse:
            result.extend(reverse[t])
        else:
            result.append(t)

    return result


def append_box(key, tokens):
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
          "text": ""
        }
      box_map[key]["examples"][sky]["count"] += 1  
      box_map[key]["examples"][sky]["text"] = tokens

def trim_sp(src):
    tok = []
    i = -1
    for c in src:
      i += 1
      if (c != 'sp'):# and c != ','):
        #print(c)
        tok.append(c)
    return tok

def trim_sp2(src,l):
    tok = []
    i = -1
    if len(linesT[i]) == len(src):
        return src
    for c in src:
      i += 1
      if i == 1 and (src[i] in {'CD','NN','VRB','IN'}) and src[0]=='LS':
        continue # and c != ','):
      elif i == 4 and (src[i-1] == 'CD' and src[i] == 'CD'):
        continue # and c != ','):
      else:
        tok.append(c)
    return tok


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

def validate_Ngrams_core(tokens, toktxt, candidates, ngm, counter):
    for i, win in sliding_windows(tokens, ngm):
        g = tuple(win)
        if g in candidates:
            tx = toktxt[i:i+ngm]
            append_box(g, tx)
            counter[g] += 1


def xxxvalidate_Ngrams(src, candidates, ngm=6):
    # candidates は必ず set にしておく
    #cand = set(candidates)
    cand = set(tuple(i) for i in candidates)

    counter = Counter()

    for toks in src:
        if len(toks) < ngm:
            continue

        # ループ外で一度だけ展開
        tokens = unzipTH(toks, 0)
        toktxt = unzipTH(toks, 1)

        # スライスを避けて tuple を逐次構築
        # 先頭の ngm 個で初期ウィンドウを作る
        window = tuple(tokens[:ngm])

        # 最初のウィンドウをチェック
        if window in cand:
            append_box(window, toktxt[:ngm])
            counter[window] += 1

        # ローリングウィンドウ方式
        for i in range(1, len(tokens) - ngm + 1):
            # window = tuple(tokens[i:i+ngm]) を避ける
            window = window[1:] + (tokens[i+ngm-1],)

            if window in cand:
                append_box(window, toktxt[i:i+ngm])
                counter[window] += 1

    return counter

def validate_Ngrams(src, cand_by_len):
    counter = Counter()

    for toks in src:
        tokens = unzipTH(toks, 0)
        toktxt = unzipTH(toks, 1)
        L = len(tokens)

        # すべての長さの候補について検定
        for ngm, candset in cand_by_len.items():
            if L < ngm:
                continue

            # 初期ウィンドウ
            window = tuple(tokens[:ngm])
            if window in candset:
                append_box(window, toktxt[:ngm])
                counter[window] += 1

            # ローリングウィンドウ
            for i in range(1, L - ngm + 1):
                window = window[1:] + (tokens[i+ngm-1],)
                if window in candset:
                    append_box(window, toktxt[i:i+ngm])
                    counter[window] += 1

    return counter


def ngrams(tokens, n=4):
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]


def make_ngrams(seq, n):
    return [tuple(seq[i:i+n]) for i in range(len(seq)-n+1)]

def nx_ngram(pos_seq, n=10):
    key = compress(pos_seq)  # cdhd+cd+nnt を合体
    return make_ngrams(key, n)            # 10-gram を取る

def ngram_freq(tokens, n=4):
    # tokens は 1行分のトークン列（リスト）
    counter.update(nx_ngram(tokens, n))

def unzipTH(cols,pos):
    tmp = []
    for t, h in cols:
        if pos == 0:
          tmp.append(t)
        else:  
          tmp.append(h)
    return tmp
      
def get_pattern(lines,no):
    i = 0
    for cols in lines:      
        if len(cols) < 4:
          continue
        co = unzipTH(cols, no)
        #print(co)
        ngram_freq(co, 4)
        i += 1
        #if i > 100:
        #    return

NOISE = {'(', ')', ',', '.', 'sp', ';', ':'}
CODE = {'cdhd', 'cd', 'CD', 'DT', 'NNP'} #, 'nnt'}

def is_noise(gram):
    return any(tok in NOISE for tok in gram)

def is_code(gram):
    return any(tok in CODE for tok in gram)

def classify_ccg(tags):
    # NP/NP
    if tags[0] in {"IN", "TO", "助副", "格", "vb"}:
        return "NP/NP"

    # NP\NP
    if tags[-1] in {"の"} or tags[0] in {"JJ", "WDT"}:
        return "NP\\NP"

    # S\NP
    if tags[-1] in {"VB", "VBN", "助動","vb"}:
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
    if tags[0] in {"cc","cd","cd1","sp","vb","nnt","nnr","nnjv","vbt",
                   "の","格","記号,空白","副","rl",
                   "接","助動","助詞,副助詞／並立助詞／終助詞"}:
        return None

    if tags[-1] in {"cc","cd","cd1","sp","vb",
                    "の","格","記号,空白","接","係",
                    "助動","助詞,副助詞／並立助詞／終助詞",
                    "cdhd","vbo","vbt","efl","ecc","r1"}:
        return None

    if "sp" in tags or "記号,空白" in tags:
        return None

    return "Okay"

def expand_ADDR(tokens):
    """
    tokens: ['ADDR','ADDR','nn','格', ...]
    戻り値: ['cdhd','cd','nnt','cdhd','cd','nnt','nn','格', ...]
    """
    expanded = []
    for t in tokens:
        if t == 'ADDR':
            expanded.extend(['cdhd', 'cd', 'nnt'])
        else:
            expanded.append(t)
    return expanded

from collections import defaultdict

def group_candidates_by_length(candidates):
    groups = defaultdict(set)
    for cand in candidates:
        groups[len(cand)].add(tuple(cand))
    return groups

if __name__ == "__main__":
    #load_src("../act-monad/data/tsv/ja1", 7)
    #load_src("../act-monad/data/tsv/en1", 7)
    #write_file("jp_list.txt",linesTH)
    #write_file("en_list.txt",linesTH)
    #loader("jp_list.txt",linesTH)
    loader("jp_list_test.txt",linesTH)
    print(f"data: text length={len(linesTH)}")
    #for tmp in linesTH:
    #    print(tmp)
    print("POSをロード完了")
    get_pattern(linesTH,0)
    print("POSをNX-gram実行完了")

    MX = 50#00
    START = 0
    # すでに抽出済みの 4-gram 頻度（例）
    # 実際にはあなたの counter.most_common() の結果を使う
    fourgram_freq = counter.most_common(MX)

    # 4-gram 部分だけ取り出す
    fourgrams = [g for (g, c) in fourgram_freq]

    # 有用な 4-gram のみ抽出
    useful_4grams = [g for g in fourgrams if is_useful_4gram(g)]

    # 4+4-2 で 6-gram 仮説生成
    candidates6 = make_Ngram_candidates(useful_4grams,2,6)
    candidates10 = make_Ngram_candidates(candidates6,2,10)
    candidates18 = make_Ngram_candidates(candidates10,4,16)
    print("POSをNX-gramを合成")

    candidatesA = decompress_list(candidates6)
    candidates = group_candidates_by_length(candidatesA)
    print("POSの合成を分解完了")
    #for tmp in candidates:
    print(f"length= {len(candidates)}")

    # 生データで検定
    #file = "../act-monad/data/stxen.txt"
    validated = validate_Ngrams(linesTH, candidates)
    print("POSのパターンでテキストを取り出し完了")

    # 出現頻度順に表示
    i = 1
    p = -1
    cnt = 0
    for g, c in validated.most_common(MX):
        p += 1
        if p < START:
          continue

        #if box_hantei(g) == None:
        #    continue
        cnt += c
        ccg = classify_ccg(g)
        print("-------------------------------------")
        print(g, c, ccg, cnt, i)
        i += 1    
        #for g in box_map[g]:
        #  if is_code(g):
        #    print(g, i)
        cc = 0
        for ex in box_map[g]["examples"]:
            print(box_map[g]["examples"][ex])
            if cc > 10:  break
            cc += 1

      #if i > 20: break
      #i += 1    
