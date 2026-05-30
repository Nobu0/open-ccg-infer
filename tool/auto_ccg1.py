
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

def loader(file, buf):
    with open(file, encoding="utf-8") as f:
      for line in f:
        tokens = line.strip().split()
        buf.append(tokens)

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

NOISE = {'(', ')', ',', '.', 'sp', ';', ':'}


def is_noise(gram):
    return any(tok in NOISE for tok in gram)

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

if __name__ == "__main__":
    file = "../act-monad/data/stxen.txt"
    file = "../act-monad/data/stxja.txt"
    file2 = "../act-monad/data/srcja.txt"
    #file = "stxja100.txt"
    #file2 = "srcja100.txt"
    loader(file, linesH)
    print(f"data: hinshi length={len(linesH)}")
    loader(file2,linesT)
    print(f"data: text length={len(linesT)}")
    get_pattern(linesH)

    連体修飾候補 = []
    述語候補 = []
    副詞句候補 = []
    チャンク境界 = []
    for g, c in counter.most_common(200):
        if is_noise(g):  continue
        if g[-1] == 'の':
          連体修飾候補.append(g)
        if g[-2] == '格' and g[-1] in ('vb','助動'):
          述語候補.append(g)
        if g[0] == 'vb' and g[-1] == '格':
          副詞句候補.append(g)
        if g[:3] == ('cdhd','cd','nnt'):
          チャンク境界.append(g)
    
    print(f"連体修飾候補 = {連体修飾候補}")
    print(f"述語候補 = {述語候補}")
    print(f"副詞句候補 = {副詞句候補}")
    print(f"チャンク境界 = {チャンク境界}")

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
    for g, c in validated.most_common(1):
        ccg = classify_ccg(g)
        print(g, c, ccg)
    i = 0    
    for g in box_map:
        print(g, i)
        c = 0
        for ex in box_map[g]["examples"]:
            print(box_map[g]["examples"][ex])
            if c > 10:  break
            c += 1
        #if i > 2: break
        i += 1    
