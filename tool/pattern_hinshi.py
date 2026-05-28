
import os
import re
from collections import Counter

counter = Counter()

from collections import Counter, defaultdict

# ノイズ語
NOISE = {'(', ')', ',', '.', 'sp'}

# 4-gram が有用かどうか判定
def is_useful_4gram(g):
    # ノイズを含むものは除外
    if any(tok in NOISE for tok in g):
        return False
    return True

# 4-gram の結合（4+4-2 = 6）
def make_6gram_candidates(fourgrams):
    candidates = set()
    fg_list = list(fourgrams)

    for a in fg_list:
        for b in fg_list:
            # a = (t1,t2,t3,t4)
            # b = (t3,t4,t5,t6) を探す
            if a[2] == b[0] and a[3] == b[1]:
                six = (a[0], a[1], a[2], a[3], b[2], b[3])
                candidates.add(six)
    return candidates

# 生データで 6-gram を検定
def validate_6grams(file, candidates):
    counter = Counter()
    with open(file, encoding="utf-8") as f:
        for line in f:
            tokens = line.strip().split()
            if len(tokens) < 6:
                continue
            # 全 6-gram を走査
            for i in range(len(tokens)-6+1):
                g = tuple(tokens[i:i+6])
                if g in candidates:
                    counter[g] += 1
    return counter


def ngrams(tokens, n=4):
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def ngram_freq(tokens, n=4):
    # tokens は 1行分のトークン列（リスト）
    counter.update(ngrams(tokens, n))

def get_pattern(file):
    i = 0
    with open(file, encoding="utf-8") as f:
        for line in f:
            cols = line.strip().split()
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
    get_pattern(file)

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
    candidates = make_6gram_candidates(useful_4grams)

    # 生データで検定
    #file = "../act-monad/data/stxen.txt"
    validated = validate_6grams(file, candidates)

    # 出現頻度順に表示
    for g, c in validated.most_common(30):
        ccg = classify_ccg(g)
        print(g, c, ccg)
