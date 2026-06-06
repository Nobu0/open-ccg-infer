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
def is_noun(pos):
    return pos.startswith("nn")

def get_token(seq):
    """名詞句の最大スパンを返す"""
    tmp = []
    for c in seq:
        if c in {'sp', '(', ')', ';', '、', '。', '格', ',', '.', '記号,空白', '接', 'cc', '係', '助並'}:
            break
        tmp.append(c)
    return tuple(tmp)

def extract_max_noun_blocks(linesTH):
    blocks = {}  # key: 名詞句タプル, value: (freq, max_flag)

    for line in linesTH:
        pos_seq = [pos for (pos, word) in line]
        n = len(pos_seq)
        i = 0

        while i < n:
            if is_noun(pos_seq[i]):
                # 最大句を取得
                key = get_token(pos_seq[i:])

                if len(key) > 1:
                    if key not in blocks:
                        blocks[key] = [0, 1]  # freq, max_flag
                    blocks[key][0] += 1

                # 名詞列をスキップ
                while i < n and is_noun(pos_seq[i]):
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
    seqs = extract_max_noun_blocks(linesTH)

    # ★ ソート＋クリーン化
    #cleaned = clean_and_sort(noun_seqs)

    # ★ 表示（品詞列だけ）
    print("=== 品詞列 ===")
    for buf in seqs:
        print(buf, seqs[buf])
    #for seq, freq in seqs:
    #    print(f"'{seq}' {freq}")

