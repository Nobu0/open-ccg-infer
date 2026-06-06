import sys
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

def is_noun301(pos):
    #if len(pos) > 2 and pos[0].startswith("nn") and pos[0] not in {'nnt','nnh','nnd','nnr'}: 
    if len(pos) > 2 and pos[0] in {"nn","nns","nnhd"}: 
       return True
    return False

def get_token301(seq):
    """名詞句の最大スパンを返す"""
    tmp = []
    if len(seq) <= 1:
        return seq
    tmp.append(seq[0])
    for c in seq[1:]:
        if tmp[-1] in {"nns"} and c in {"nnt"}:        
            tmp.append(c)
            break
        elif c in {"nn","の"}:        
            tmp.append(c)
        else:
            break
    if tmp[-1] in {"nn"}:
        return tmp
    else:
        if len(tmp) > 1:
            tmp.pop()
        return tmp

def is_noun302(pos):
    if len(pos) > 2 and (pos[0].startswith("nn") and pos[0] not in {'nnt'}): 
       return True
    return False

def get_token302(seq):
    """名詞句の最大スパンを返す"""
    tmp = []
    if len(seq) <= 1:
        return seq
    tmp.append(seq[0])
    for c in seq[1:]:
        if c in {"nnt"}:
            tmp.append(c)
            break
        elif c.startswith("nn") or c in {'の'}:        
            tmp.append(c)
        else:
            break
    if tmp[-1].startswith("nn"):
        return tmp
    else:
        if len(tmp) > 1:
            tmp.pop()
        return tmp

def extract_max_noun_blocks301(linesTH):
    blocks = {}  # key: 名詞句タプル, value: (freq, max_flag)

    for line in linesTH:
        pos_seq = [pos for (pos, txt) in line]
        txt_seq = [txt for (pos, txt) in line]
        n = len(pos_seq)
        i = 0

        while i < n:
            if is_noun301(pos_seq[i:]):
                # 最大句を取得
                key = get_token301(pos_seq[i:])
                sl = len(key)
                
                if len(key) > 1:
                    key = tuple(key)
                    append_box(key, txt_seq[i:i+sl])
                    if key not in blocks:
                        blocks[key] = [0, 1]  # freq, max_flag
                    blocks[key][0] += 1
                    i += sl
                else:
                  i += sl                
                  # 名詞列をスキップ
                  while i < n and is_noun301(pos_seq[i]):
                      i += 1
            else:
                i += 1

    return blocks

def extract_max_noun_blocks302(linesTH):
    blocks = {}  # key: 名詞句タプル, value: (freq, max_flag)

    for line in linesTH:
        pos_seq = [pos for (pos, txt) in line]
        txt_seq = [txt for (pos, txt) in line]
        n = len(pos_seq)
        i = 0

        while i < n:
            if is_noun302(pos_seq[i:]):
                # 最大句を取得
                key = get_token302(pos_seq[i:])
                sl = len(key)
                
                if len(key) > 1:
                    key = tuple(key)
                    append_box(key, txt_seq[i:i+sl])
                    if key not in blocks:
                        blocks[key] = [0, 1]  # freq, max_flag
                    blocks[key][0] += 1
                    i += sl
                else:
                  i += sl                
                  # 名詞列をスキップ
                  while i < n and is_noun302(pos_seq[i]):
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
    args = sys.argv

    print(f"実行ファイル名: {args[0]}")
    print(f"第1引数: {args[1]}")

    loader("jp_list.txt", linesTH)
    #loader("jp_list_test.txt", linesTH)
    print(f"data: text length={len(linesTH)}")
    print("POSをロード完了")

    if args[1] == "301":

      # ★ 名詞列の元ネタ抽出
      #seqs = extract_max_noun_blocks302(linesTH)
      seqs = extract_max_noun_blocks301(linesTH)

      MX = 100
      # ★ 表示（品詞列だけ）
      print("=== 品詞列 ===")
      for g in seqs:
          print(g, seqs[g])
          cc = 0
          for ex in box_map[g]["examples"]:
              print(box_map[g]["examples"][ex])
              if cc > 10:  break
              cc += 1

    elif args[1] == "302":

      # ★ 名詞列の元ネタ抽出
      seqs = extract_max_noun_blocks302(linesTH)
      #seqs = extract_max_noun_blocks301(linesTH)

      MX = 100
      # ★ 表示（品詞列だけ）
      print("=== 品詞列 ===")
      for g in seqs:
          print(g, seqs[g])
          cc = 0
          for ex in box_map[g]["examples"]:
              print(box_map[g]["examples"][ex])
              if cc > 10:  break
              cc += 1


    #for seq, freq in seqs:
    #    print(f"'{seq}' {freq}")
