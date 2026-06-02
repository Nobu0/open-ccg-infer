import sqlite3
import os


def file_to_db(cur, path, i, lang):
        if not os.path.exists(path):
            return
        print(path)
        # 1. ファイルの読み込み
        with open(path, 'r', encoding='utf-8') as f:

          for line in f:
              line = line.replace('\t', ' ')
              line = line.replace('\u3000', ' ')  # 全角スペース
              line = line.strip()
              toks = line.split()
              if len(toks) <= max(7, 6):
                  continue

              # 3. pos_tbl への登録
              cur.execute("""
                  INSERT INTO pos_tbl (act_id, lang, line_num, word, pos)
                  VALUES (?, ?, ?, ?, ?)
              """, (i, lang, toks[2], toks[6], toks[7]))

# 形態素ファイルをDBにインポートする
def import_pos_to_db(db_path, data_dir):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 対象のファイルリスト（src_1.txt 〜 src_634.txt）
    for i in range(1, 635):
        jp_file = f"ja1/src_{i}.txt"
        en_file = f"en1/src_{i}.txt" # 英語ファイル名の形式に合わせて調整してください
        jp_path = os.path.join(data_dir, jp_file)
        en_path = os.path.join(data_dir, en_file)
        file_to_db(cur, jp_path, i, 'jp')
        file_to_db(cur, en_path, i, 'en')

    conn.commit()
    conn.close()
    print("Import completed.")

# 実行例
# --- 設定と実行 ---
if __name__ == "__main__":
    import_pos_to_db('db/ccgDB.sqlite', '../act-monad/data/tsv/')
