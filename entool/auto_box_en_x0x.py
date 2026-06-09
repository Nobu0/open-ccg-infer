import sqlite3
from collections import defaultdict
import sys
import time



PAT_CLASS = {
    101:  {'typ':'#ADDR_ART', 'nam':'条（Article）'},
    102:  {'typ':'#ADDR_PAR', 'nam':'項（Paragraph）'},
    103:  {'typ':'#ADDR_NUM', 'nam':'号（Item Number）'},
    104:  {'typ':'#ADDR_PAT', 'nam':'編（Part）'},
    105:  {'typ':'#ADDR_CHA', 'nam':'章（Chapter）'},
    106:  {'typ':'#ADDR_SEC', 'nam':'節（Section）'},
    107:  {'typ':'#ADDR_SUB', 'nam':'款（Subsection）'},
    108:  {'typ':'#ADDR_DIV', 'nam':'目（Division）'},
    201:  {'typ':'#FIXED_PP', 'nam':'英語の固定前置詞句'},
    202:  {'typ':'#FIXED_INF','nam':'英語の不定詞句'},
    301:  {'typ':'', 'nam':"名詞句 (SIMPLE)" },
    302:  {'typ':'', 'nam':"名詞句（REL）" },
    303:  {'typ':'', 'nam':"アドレスを含む名詞句、数詞を含む(ADDR)" },
    304:  {'typ':'', 'nam':"法令での名詞句等(OTHER)" },
    305:  {'typ':'', 'nam':"その他の名詞句等(REFER)" },
}

DESC ="品詞列等に基づく BOX 化"

TXT1 =  {('Article'):   101,
        ('Art'):        101,
        ('paragraph'):  102,
        ('item'):       103,
        ('Part'):       104,
        ('Chapter'):    105,
        ('Section'):    106,
        ('Subsection'): 107,
        ('Division'):   108,}

PAT2 = {('DT', 'NN'): 301,
        ('NN', 'NN'): 301,
        ('JJ', 'NN'): 301,
        ('NNP', 'NNP'):301,}

PAT3 = {
      ('IN', 'NN', 'IN'): 201,
      ('TO', 'VB', 'VBN'): 302,
      ('NNP', 'NNP', 'CD'): 303,
      ('NNP', 'CD', 'CD'): 303,
}

PAT4 = {
      ('TO', 'VB', 'VBN'): 302,
      ('NNP','CD',',','CD'):303,
}

PAT6 ={
      ('IN', 'DT', 'NN', 'IN', 'DT', 'NN'):302,
      ('DT', 'NN', 'IN', 'DT', 'JJ', 'NN'):302,
      ('NN', 'IN', 'DT', 'NNP', 'IN', 'NNP'):302,
      ('VBN', 'IN', 'DT', 'NN', 'IN', 'DT'):302,
      ('MD',  'VB', 'VBN', 'TO', 'VB', 'VBN'):302,
      ('NN', 'NN', 'JJ', 'TO', 'NNP', 'CD'):302,
}

PAT7 ={
      ('JJ', 'TO', 'DT', 'NNS', 'IN', 'DT', 'NN'):302,
}

PAT8 ={
      ('DT', 'NN', 'IN', 'DT', 'NN', 'IN', 'DT', 'NN'):302,
}

PAT_ALL = {**PAT2, **PAT3, **PAT4, **PAT6, **PAT7, **PAT8}

class Matches:

    def seq2(self, pos_seq, txt_seq):
        # 特殊ケース（Article 27 など）
        if pos_seq[0] in {'NNP','NN'} and pos_seq[1] in {'CD','NNP','LS'} and txt_seq[0] in TXT1:
            return TXT1[txt_seq[0]]

        key = (pos_seq[0], pos_seq[1])
        return PAT2.get(key)

    def seqN(self, pos_seq):
        key = tuple(pos_seq)
        return PAT_ALL.get(key)


def insert_box_line(pos_seq, txt_seq, id_seq):
    obj = Matches()
    result = []
    mx = len(pos_seq)
    c = 0

    NGRAMS = [8,7,6,4,3,2]

    while c < mx:
        matched = False

        for n in NGRAMS:
            if c + n > mx:
                continue

            if n == 2:
                class_id = obj.seq2(pos_seq[c:c+2], txt_seq[c:c+2])
            else:
                class_id = obj.seqN(pos_seq[c:c+n])

            if class_id:
                result.append([
                    class_id,
                    pos_seq[c:c+n],
                    txt_seq[c:c+n],
                    id_seq[c:c+n]
                ])
                c += n
                matched = True
                break

        if not matched:
            c += 1

    return result


def process_pos_rows(cur, act, lang):
    # pos_tbl から行を取得
    cur.execute("""
        SELECT src_id, line_num, pos, word
        FROM pos_tbl
        WHERE act_id = ? AND lang = ?
        ORDER BY src_id
    """, (act,lang,))
    rows = cur.fetchall()

    # pos_seq / txt_seq / id_seq を作成
    pos_seq = [r[2] for r in rows]
    txt_seq = [r[3] for r in rows]
    id_seq  = [r[0] for r in rows]

    # BOX 抽出
    boxes = insert_box_line(pos_seq, txt_seq, id_seq)

    # insert_buffer を作成
    insert_buffer = []
    for class_id, pseq, tseq, ids in boxes:
        start_id = ids[0]
        end_id   = ids[-1]
        content  = " ".join(tseq)
        msg = PAT_CLASS[class_id]
        addm = ""
        if len(msg['typ'])> 0:
            addm = f" {msg['typ']}"
        type = " ".join(pseq)  # 300番台は純粋な品詞列、他は後でマーク付与
        box_type = f"{type}{addm}"

        insert_buffer.append((
            act,          # act_id
            lang,            # lang（英語=1）
            start_id,
            end_id,
            content,
            class_id,
            box_type
        ))

    return insert_buffer


def batch_box(conn, act_id=None, lang=2, batch_size=1000):

    cur = conn.cursor()

     # ----------------------------------------
    # 2. 対象 act_id の一覧を取得
    # ----------------------------------------
    if act_id is None:
        cur.execute("SELECT DISTINCT act_id FROM pos_tbl ORDER BY act_id")
        act_list = [row[0] for row in cur.fetchall()]
    else:
        act_list = [act_id]

    total_box = 0
    total_width = 0

    # ----------------------------------------
    # 3. act_id ごとに BOX 化
    # ----------------------------------------
    for act in act_list:
        print(f"act_id = {act}")
        act_box_count = 0
        act_width_sum = 0

        insert_buffer = process_pos_rows(cur, act, lang)

        # BOX 数
        act_box_count += len(insert_buffer)

        # 幅の合計
        for row in insert_buffer:
            start_id = row[2]
            end_id   = row[3]
            act_width_sum += (end_id - start_id + 1)

        # バッチサイズに達したらまとめて INSERT
        if len(insert_buffer) >= batch_size:
            cur.executemany("""
                INSERT OR IGNORE INTO box_tbl
                    (act_id, lang, start_id, end_id, content, class_id, box_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, insert_buffer)
            insert_buffer.clear()

        try:
          # 残りをフラッシュ
          if insert_buffer:
              cur.executemany("""
                  INSERT OR IGNORE INTO box_tbl
                      (act_id, lang, start_id, end_id, content, class_id, box_type)
                  VALUES (?, ?, ?, ?, ?, ?, ?)
              """, insert_buffer)
              insert_buffer.clear()

        except Exception as e:
            print("変換エラー:", insert_buffer, e)

        total_box   += act_box_count
        total_width += act_width_sum

        # act_id 単位で COMMIT
        conn.commit()
        end_time = time.perf_counter()
        # 所要時間の計算（秒）
        elapsed_time = end_time - start_time
        print(f"所要時間: {elapsed_time:.4f} 秒: {total_box} {total_width}")

    return total_box, total_width


def batch__history(conn, total_box, total_width=0, act_id=None, lang=1, name="BOX batch", desc="pos_box_tbl patterns"):
    cur = conn.cursor()

    # -----------------------------
    # 4. BOX 統計の計算
    # -----------------------------
    if total_box > 0:
        box_ave = total_width / total_box
    else:
        box_ave = 0

    # 重なり率（簡易版：BOX 数 / pos 数）
    cur.execute("SELECT COUNT(*) FROM pos_tbl")
    all_pos = cur.fetchone()[0]

    if all_pos > 0:
        box_ovlp = total_box / all_pos
    else:
        box_ovlp = 0

    # 位置率（BOX の start_id の平均位置）
    cur.execute("SELECT AVG(start_id) FROM box_tbl")
    avg_pos = cur.fetchone()[0] or 0
    box_hed = (avg_pos / all_pos) * 100 if all_pos > 0 else 0

    # -----------------------------
    # 5. his_box_tbl に履歴登録
    # -----------------------------
    cur.execute("""
        INSERT INTO his_box_tbl
        (act_id, name, desc, lang, all_pos, box_cnt, box_ave, box_hed, box_ovlp, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        act_id if act_id else -1,
        name,
        desc,
        lang,
        all_pos,
        total_box,
        box_ave,
        box_hed,
        box_ovlp,
        1
    ))

    conn.commit()

    print("BOX 化完了:", total_box, "件")
    print("平均幅:", box_ave)
    print("重なり率:", box_ovlp)
    print("位置率:", box_hed)

def main_box(conn):

  # sys.argvには、実行時の引数が「文字列のリスト」として格納されます
  args = sys.argv

  print(f"実行ファイル名: {args[0]}")
      
  total_box,total_width = batch_box(
      conn,
      act_id=None,          # 全法令
      lang=2               # 英語
  )
  print(total_width)

  batch__history(conn,
      total_box,
      total_width,
      act_id=None,
      lang=2,
      name="ADDRや名詞句",
      desc="pos_box_tbl に基づくアドレス句 BOX 化"
      )


#################################
# 自動登録定型パターン
#################################
# 開始時間の取得
start_time = time.perf_counter()

conn = sqlite3.connect("db/ccgDB.sqlite")

main_box(conn)

end_time = time.perf_counter()
# 所要時間の計算（秒）
elapsed_time = end_time - start_time
print(f"所要時間: {elapsed_time:.4f} 秒")
