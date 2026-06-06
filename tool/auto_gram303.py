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


class Matches:

    def seq2(self,pos_seq, txt_seq):
        #print(pos_seq,txt_seq)
        if pos_seq[0] in ('cd') and txt_seq[1] in {"条", "号", "項", "段"}:
            return (pos_seq, txt_seq)
        return (None, None)


    def seq3(self,pos_seq, txt_seq):
        # 例：['cdhd','cd','nnt'] → 第百一号
        if pos_seq[0:2] == ['cdhd', 'cd'] and pos_seq[2] in {'nnt','nnr'}:
            return (pos_seq, txt_seq)
        return (None, None)


    def seq4(self,pos_seq, txt_seq):
        # 例：['nns','格','vb','nnh'] → 管理を図るため
        if pos_seq == ['nns','格','vb','nnh'] and txt_seq[3].endswith("ため"):
            return (pos_seq, txt_seq)
        if pos_seq == ['nn', '格','vb','nnh']:
            return (pos_seq, txt_seq)
        return (None, None)

    def seq5(self,pos_seq, txt_seq):
        if pos_seq == ['nn', 'nn', '格','vb','nnh'] and txt_seq[0] != "つて":
            return (pos_seq, txt_seq)
        return (None, None)

    def seq6(self,pos_seq, txt_seq):
        if pos_seq == ['nnp', 'cd', 'nnt', 'nnr', 'cd', 'nnt']:
            return (pos_seq, txt_seq)
        return (None, None)

def is_np_addr(pos_seq, txt_seq):
    """
    pos_seq: ['cdhd','cd','nnt'] のような品詞列
    text: '第百一号' のような表層文字列
    """
    obj = Matches()

    for i in {4,3,2,5,6}: 
      if len(pos_seq) >= i:
        func = getattr(obj, f"seq{i}")
        (pos, txt) = func(pos_seq[0:i], txt_seq[0:i])
        if txt != None:
          return (pos,txt)

    return (None, None)


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


def extract_pattern_blocks303(linesTH):
    blocks = {}  # key: 名詞句タプル, value: (freq, max_flag)

    for line in linesTH:
        pos_seq = [pos for (pos, txt) in line]
        txt_seq = [txt for (pos, txt) in line]
        n = len(pos_seq)
        i = 0

        while i < n:
            (key, txt) = is_np_addr(pos_seq[i:], txt_seq[i:])
            if key != None:
                sl = len(key)
                tag = tuple(key)
                #print(tag, txt)
                if tag not in blocks:
                   blocks[tag] = 1
                else:   
                   blocks[tag] += 1
                append_box(tag, txt)
                i += sl
            else:
                i += 1

    return blocks


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
    seqs = extract_pattern_blocks303(linesTH)

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
