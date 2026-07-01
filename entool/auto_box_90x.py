import sqlite3
from collections import defaultdict
import sys
import time
from def_class_id import PAT_CLASS

DESC ="品詞列等に基づく BOX 化"


PAT_ALL = {}

def kako_recursive(txt_seq, lang):
    """
    括弧を抽出する
    """
    open_ch, close_ch = ('（', '）')
    if lang == 2:
       open_ch, close_ch = ('(', ')')
    elif lang==9: 
       open_ch, close_ch = ('-LRB-', '-RRB-')
    stack = []
    box_kakos = []
    
    i = 0
    while i < len(txt_seq):
        if txt_seq[i] == open_ch:
            #print("s: ",txt_seq[i],"/")
            stack.append(i)
        elif txt_seq[i] == close_ch:
            #print("e: ",txt_seq[i],"/")
            if stack:
                start_idx = stack.pop()
                if not stack:
                    box_kakos.append((start_idx,i+1))
                    #print(start_idx,i+1,txt_seq[start_idx:i+1])
                    #kako_id_counter += 1
        i += 1

    return box_kakos

def boxer_recursive(txt_seq, lang):
    """
    ",「」を抽出する
    """
    open_ch, close_ch = ('""""', '""""')
    if lang == 1:
        open_ch, close_ch = ('「', '」')
    stack = []
    boxs = []
    
    i = 0
    while i < len(txt_seq):
        if txt_seq[i] == open_ch and not stack:
            #print("s: ",txt_seq[i])
            stack.append(i)
        elif txt_seq[i] == close_ch:
            #print("e: ",txt_seq[i])
            if stack:
                start_idx = stack.pop()
                boxs.append((start_idx,i+1))
                #print(start_idx,i+1,txt_seq[start_idx:i+1])
                #kako_id_counter += 1
        i += 1

    return boxs

def insert_box_line(lang,pos_seq, txt_seq, id_seq):
    result = []

    boxs = kako_recursive(txt_seq, lang)
    for s,e in boxs:
      result.append((900,pos_seq[s:e],txt_seq[s:e],id_seq[s:e]))

    boxs = kako_recursive(pos_seq, 9)
    for s,e in boxs:
      result.append((900,pos_seq[s:e],txt_seq[s:e],id_seq[s:e]))

    boxs = boxer_recursive(txt_seq, lang)
    for s,e in boxs:
      result.append((901,pos_seq[s:e],txt_seq[s:e],id_seq[s:e]))

    return result


def process_pos_rows(cur, act, lang):
    cur.execute("""
    SELECT src_id, line_num, pos, word
    FROM pos_tbl
    WHERE act_id = ? AND lang = ?
    ORDER BY line_num, src_id
    """, (act, lang))

    rows = cur.fetchall()

    # 行番号ごとにまとめる
    from collections import defaultdict

    line_map = defaultdict(list)

    for src_id, line_num, pos, word in rows:
        line_map[line_num].append((src_id, pos, word))

    insert_buffer = []

    # 行ごとに pos_seq / txt_seq / id_seq を作成
    for line_num, items in line_map.items():
        id_seq  = [sid for sid, pos, word in items]
        pos_seq = [pos for sid, pos, word in items]
        txt_seq = [word for sid, pos, word in items]

        # BOX 抽出
        boxes = insert_box_line(lang, pos_seq, txt_seq, id_seq)

        # insert_buffer を作成
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
            #print(start_id,end_id,class_id,content,box_type)
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
