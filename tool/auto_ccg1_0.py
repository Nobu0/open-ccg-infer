
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

box_map = {}

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

def loader(file, buf, flg):
    with open(file, encoding="utf-8") as f:
      l = -1
      for line in f:
        l += 1
        tokens = line.strip().split()
        if flg == 1:
            tok = trim_sp(tokens)
        elif flg == 2:
            tok = trim_sp2(tokens,l)
        else:
            tok = tokens
        buf.append(tok)

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


# 生データで N-gram を検定
def validate_Ngrams(linesH, candidates, ngm):
    counter = Counter()
    l = -1
    for tokens in linesH:
        l += 1     
        if len(tokens) < ngm:
            continue
        # 全 6-gram を走査
        for i in range(len(tokens)-ngm+1):
            g = tuple(tokens[i:i+ngm])
            if g in candidates:
                tx = linesT[l][i:i+ngm]
                append_box(g, tx) 
                counter[g] += 1
    return counter


def ngrams(tokens, n=4):
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def ngram_freq(tokens, n=4):
    # tokens は 1行分のトークン列（リスト）
    counter.update(ngrams(tokens, n))

def get_pattern(linesH):
    i = 0
    for cols in linesH:
        if len(cols) < 4:
            continue
        ngram_freq(cols, 4)
        i += 1
        #if i > 100:
        #    return

def cnv_address(linesH, lineT):
    i = 0
    for cols in linesH:
        i += 1

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

def check_HT():
    i = -1
    for x in linesH:
        i += 1
        if len(linesH[i]) != len(linesT[i]):
            print (i, linesH[i])
            print (i, linesT[i])

if __name__ == "__main__":
    #file = "../act-monad/data/stxja.txt"
    #file2 = "../act-monad/data/srcja.txt"
    file = "../act-monad/data/stxen.txt"
    file2 = "../act-monad/data/srcen.txt"
    #file = "stxja100.txt"
    #file2 = "srcja100.txt"
    loader(file2,linesT, 0)
    print(f"data: text length={len(linesT)}")
    loader(file, linesH, 2)
    print(f"data: hinshi length={len(linesH)}")
    check_HT()
    exit

    cnv_address(linesH, linesT)
    get_pattern(linesH)

    # すでに抽出済みの 4-gram 頻度（例）
    # 実際にはあなたの counter.most_common() の結果を使う
    fourgram_freq = counter.most_common(200)

    # 4-gram 部分だけ取り出す
    fourgrams = [g for (g, c) in fourgram_freq]

    # 有用な 4-gram のみ抽出
    useful_4grams = [g for g in fourgrams if is_useful_4gram(g)]

    # 4+4-2 で 6-gram 仮説生成
    candidates = make_Ngram_candidates(useful_4grams,2,6)
    #candidates1 = make_Ngram_candidates(candidates0,2,10)
    #candidates = make_Ngram_candidates(candidates1,2,18)

    # 生データで検定
    #file = "../act-monad/data/stxen.txt"
    validated = validate_Ngrams(linesH, candidates, 6)

    # 出現頻度順に表示
    for g, c in validated.most_common(20):
      #if is_code(g):
        ccg = classify_ccg(g)
        print("-------------------------------------")
        print(g, c, ccg)
        #continue
        i = 0    
        #for g in box_map[g]:
        #  if is_code(g):
        #    print(g, i)
        c = 0
        for ex in box_map[g]["examples"]:
            print(box_map[g]["examples"][ex])
            if c > 100:  break
            c += 1

      #if i > 20: break
      #i += 1    
