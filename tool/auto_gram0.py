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

nn_list = {
'nns',
'nn',
'nnt',
'nnh',
'nnr',
'nn nn',
'nns nnt',
'nn nnt',
'nns nn',
'nnjv',
'nn nns',
'nns nns',
'nnhd nn',
'nnp',
'nn nn nn',
'nnd',
'nn nns nnt',
'nn nns nn',
'nnt nn',
'nn nn nnt',
'nns nns nnt',
'nns nn nnt',
'nn nnt nnt',
'nnt nnh',
'nnt nnt',
'nns nns nn',
'nn nn nns nnt',
'nns nn nn',
'nnhd nnt',
'nns nns nns',
'nnt nnr',
'nnp nnt',
'nns nnr',
'nnhd nn nnt',
'nnt nnhd nnt',
'nnhd',
'nnhd nnd',
'nnr nnt',
'nnjv nn',
'nnhd nns nnt',
'nnhd nns',
'nnhd nn nn',
'nnjv nnt',
'nnp nn',
'nnh nnjv',
'nnh nn',
'nnjv nns',
'nnr nns',
'nnt nns',
'nnhd nn nn nnt',
'nnr nnh',
'nnhd nns nn',
'nnjv nn nnt',
'nnjv nns nns',
'nnh nnd',
'nnjv nns nnt',
'nnh nns',
'nnt nnp nnt',
'nnh nnr',
'nnr nn',
'nnp nnp',
'nnjv nn nn',
'nnjv nns nn nnt',
'nnp nn nn',
'nnt nnp',
'nnr nnr',
'nnt nn nnt',
'nnjv nns nn',
'nnr nn nn',
'nnr nn nnhd nnt',
'nnp nn nn nnt',
'nnh nn nn',
'nnd nn',
'nnp nn nnt',
'nnp nn nns nnt',
'nnr nnhd nn',
'nnh nnh',
'nnp nnp nnt',
'nnr nns nnt',
'nnp nns nn',
'nnh nnt',
'nnd nns',
'nnh nn nnt',
'nnd nn nn',
'nnd nn nnt nnt',
'nnd nn nn nnt',
'nnd nnjv',
'nnd nnh',
'nnd nn nns nn',
'nnjj',
'nnd nnd',
'nnjj nns',
'nnc nns nns nns nnt',
'nnc',
'nnjj nn',
'nnjj nn nn',
'nnc nnp',
'nnc nn nn',
'nnjj nns nns',
'nnjj nn nnd',
'nnjj nn nns nnt nns nns',
'nnjj nns nnt',
'nnjj nn nns nns nns nns nnt',
'nnjj nnp',
'nnc nn',
'nnc nn nn nnt',
'nnc nn nn nn',
'nnc nns nns nns nnt nnt',
}

def compress(tokens):
    i = 0
    result = []

    while i < len(tokens):
        matched = False

        for pat, _ in patterns.items():
            L = len(pat)
            if tuple(tokens[i:i+L]) == pat:
                lab = "_".join(pat) 
                #print(lab)
                result.append(lab)
                i += L
                matched = True
                break

        if not matched:
            result.append(tokens[i])
            i += 1

    return result

def decompress_list(tokens):
    buf = []
    for toks in tokens:
        lst = decompress(toks)
        buf.append(lst)
    return buf

def decompress(tokens):
    result = []
    for t in tokens:
        lst = t.split("_")
        #if len(lst) > 1:
        #    print(lst)
        result.extend(lst)

    return result

def get_token(lst):
    tmp = []
    for c in lst:
        if c in {'sp', '(',')', ';','、','。','格',',','.','記号,空白','接','cc','係','助並'}:
            break
        tmp.append(c)
    return tuple(tmp)    

def is_noun(pos):
    return pos.startswith("nn")

def extract_sequences(linesTH, max_len=20):
    blocks = {}
    for line in linesTH:
        pos_seq = [pos for (pos, word) in line]
        n = len(pos_seq)
        i = 0

        while i < n:
            if is_noun(pos_seq[i]):
                key = get_token(pos_seq[i:])
                if len(key) > 1:
                    blocks[key] = blocks.get(key, 0) + 1
                # 名詞が続く限りスキップ（ここでは20-gramを取らない）
                while i < n and pos_seq[i].startswith("nn"):
                    i += 1
            else:
                i += 1

    return blocks

def clean_and_sort(noun_sequences):

    counter = Counter(noun_sequences)
    sorted_items = counter.most_common()

    cleaned = []
    head_count = {}

    for seq, freq in sorted_items:
        head = seq.split()[0]
        if head not in head_count:
            head_count[head] = 0

        #if head_count[head] < 3:
        cleaned.append((seq, freq))
        head_count[head] += 1
    
    return sorted(cleaned)


def print_pos_sequences(pos_seq, max_lines=50):
    """
    pos_seq: [(pos, word), ...]
    max_lines: 表示する最大行数
    """
    count = 0
    current_line = []

    i = -1
    for line in pos_seq:
      for (pos, word) in line:  
        i += 1
        current_line.append(pos)

        # 句読点で行を切る（任意）
        if pos in ("。", "終", "句点"):
            print(" ".join(current_line))
            current_line = []
            count += 1
            if count >= max_lines:
                break

    # 最後の行が残っていたら出す
    if current_line:
        print(" ".join(current_line))


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


if __name__ == "__main__":
    loader("jp_list.txt", linesTH)
    #loader("jp_list_test.txt", linesTH)
    print(f"data: text length={len(linesTH)}")
    print("POSをロード完了")

    # ★ 名詞列の元ネタ抽出
    seqs = extract_sequences(linesTH, max_len=10)

    # ★ ソート＋クリーン化
    #cleaned = clean_and_sort(noun_seqs)

    # ★ 表示（品詞列だけ）
    print("=== 品詞列 ===")
    for buf in seqs:
        print(buf, seqs[buf])
    #for seq, freq in seqs:
    #    print(f"'{seq}' {freq}")

"""
if __name__ == "__main__":
    #loader("jp_list_test.txt", linesTH)
    loader("jp_list.txt", linesTH)
    print(f"data: text length={len(linesTH)}")
    print("POSをロード完了")

    # ★ 名詞ブロック抽出
    noun_blocks = extract_noun_blocks(linesTH, max_len=20)

    # ★ ソート＋クリーン化
    cleaned = clean_and_sort_blocks(noun_blocks)

    # ★ 表示（品詞列だけ）
    print("=== 名詞ブロック一覧 ===")
    for block, count in cleaned[:200]:
        print(f"{block}  ({count})")
"""