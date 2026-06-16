import ast
import re
import sqlite3

def register_pos_patterns_from_log(conn, filename, lang=2, priority=1):
    """
    filename: ログファイル（6-gram のデバッグ出力）
    lang: 1=日本語, 2=英語
    priority: 優先度
    """

    cur = conn.cursor()

    # 行頭のタプル (...) を抽出する正規表現
    tuple_re = re.compile(r"^\([^)]*\)")
    class_re = re.compile(r"(30[1-5])$")

    with open(filename, encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # 「(」で始まる行だけ処理
            if not line.startswith("("):
                continue

            # 行頭のタプル部分だけ抽出
            m = tuple_re.match(line)
            if not m:
                print("タプル抽出失敗:", line)
                continue

            class_m = class_re.search(line)
            if not class_m:
                print("class_id抽出失敗:", line)
                continue

            tuple_str = m.group(0)
            class_id = class_m.group(1)
            try:
                # "( 'cdhd','cd','nnt',... )" を tuple に変換
                tags = ast.literal_eval(tuple_str)

                # tuple → カンマ区切り文字列
                pat_tags = ",".join(tags)
                pat_len = len(tags)

                # pos_box_tbl に登録
                cur.execute("""
                    INSERT INTO pos_box_tbl (lang, pat_len, pat_tags, class_id, priority)
                    VALUES (?, ?, ?, ?, ?)
                """, (lang, pat_len, pat_tags, class_id, priority))

            except Exception as e:
                print("変換エラー:", tuple_str, e)

    conn.commit()

###############################################
conn = sqlite3.connect("db/ccgDB.sqlite")


register_pos_patterns_from_log(
    conn,
    filename="logen4_304_305.txt",  # あなたのログファイル
    lang=2,                    # 日本語
    priority=1
)

register_pos_patterns_from_log(
    conn,
    filename="logen6_304_305.txt",  # あなたのログファイル
    lang=2,                    # 日本語
    priority=1
)

conn.close()

