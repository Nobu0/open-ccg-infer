import ast
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

PATTERNS6 = {
    # 英語
    ('JJ', 'TO', 'DT', 'NNS', 'IN'):1,
    ('JJ','TO','NNP','CD'):1,
    ('NN','NN','JJ','TO'):1,
    ('NNP','NNP','NNP'):1,
    ('NN','JJ','TO'):1,
    ('NN','JJ','IN'):1,
    ('IN','DT','NN'):1,
    ('TO','DT','NN'):1,
    ('NNP','CD'):1,
    ('IN','DT'):1,
    ('TO','DT'):1,
    ('JJ','NN'):1,
    ('JJ','IN'):1,
    ('JJ','TO'):1,
}
PATTERNS = {}


def compress(tokens, patterns=PATTERNS):
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

def validate_Ngrams(src, cand_by_len):
    counter = Counter()

    for toks in src:
        tokens = [pos for (pos,txt) in toks]
        toktxt = [txt for (pos,txt) in toks]
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

def nx_ngram(pos_seq, n=10, pat=PATTERNS):
    key = compress(pos_seq, pat)  # cdhd+cd+nnt を合体
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
    if tags[0] in {"IN", "TO", "助副", "格"}:
        return "NP/NP"

    # NP\NP
    if tags[-1] in {"の"} or tags[0] in {"JJ", "WDT"}:
        return "NP\\NP"

    # S\NP
    if tags[-1] in {"VB", "VBN", "助動"}:
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
    if tags[0] in {'SP'}:
        return None

    if tags[-1] in {"SP"}:
        return None

    if "SP" in tags:
        return None

    return "Okay"


from collections import defaultdict

def group_candidates_by_length(candidates):
    groups = defaultdict(set)
    for cand in candidates:
        groups[len(cand)].add(tuple(cand))
    return groups

preps = {"in", "on", "with", "by", "for", "under", "over", "to", "of"}

def classify_ngram(text):
    t = [w.lower() for w in text]

    # FIXED_PP (201)
    if t[0] in preps and t[2] in preps:
        return 201

    # PP (501)
    if len(t) == 1 and t[0] in preps:
        return 501

    # NP_ADDR (303)
    if any(w.isdigit() for w in t):
        return 303

    # NP_REL (302)
    if any(w in preps for w in t):
        return 302

    # NP_SIMPLE (301)
    if len(t) <= 3:
        return 301

    # その他
    return 304

if __name__ == "__main__":
    #load_src("../act-monad/data/tsv/en1", 7)
    #write_file("en_list.txt",linesTH)
    #loader("en_list.txt",linesTH)
    loader("en_list_test.txt",linesTH)
    print(f"data: text length={len(linesTH)}")
    #for tmp in linesTH:
    #    print(tmp)
    print("POSをロード完了")
    get_pattern(linesTH,PATTERNS6)
    print("POSをNX-gram実行完了")

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
    candidates6 = make_Ngram_candidates(useful_4grams,2,6)
    #candidates10 = make_Ngram_candidates(candidates6,2,10)
    #candidates18 = make_Ngram_candidates(candidates10,4,16)
    print("POSをNX-gramを合成")

    candidatesA = decompress_list(candidates6)
    candidatesB = decompress_list(useful_4grams)
    candidates = group_candidates_by_length(candidatesB)
    print("POSの合成を分解完了")
    #for tmp in candidates:
    print(f"length= {len(candidates)}")

    # 生データで検定
    #file = "../act-monad/data/stxen.txt"
    validated = validate_Ngrams(linesTH, candidates)
    print("POSのパターンでテキストを取り出し完了")

    i = 1
    p = -1
    cnt = 0
    for g, c in validated.most_common(MX):
        ccg = classify_ccg(g)
        print(g, c, ccg, cnt, i, len(g))
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

        #if box_hantei(g) == None:
        #    continue
        cnt += c
        ccg = classify_ccg(g)
        print("-------------------------------------")
        print(g, c, ccg, cnt, i, len(g))
        i += 1    
        #for g in box_map[g]:
        #  if is_code(g):
        #    print(g, i)
        cc = 0
        #for ex in sorted(box_map[g]["examples"].items(), key=lambda x: x[1], reverse=True):
        #sublist = box_map[g]["examples"]
        data = [box_map[g]["examples"][ky] for ky in box_map[g]["examples"]]
        #print(data)
        sorted_data = sorted(data, key=lambda x: x['count'], reverse=True)
        for item in sorted_data:
            class_id = classify_ngram(item["text"])
            if item["count"] < 2:
                break
            print(item, class_id)
            #if cc > 10000:  break
            cc += 1

        #for info in sorted(sublist.itmes(), key=lambda x: x["count"], reverse=True):
        #    print(info)

      #if i > 20: break
      #i += 1    
