import ast
import re
import sqlite3

def register_pos_patterns_from_log(conn, filename, lang=1, class_id=100, priority=1):
    """
    filename: ログファイル（6-gram のデバッグ出力）
    lang: 1=日本語, 2=英語
    class_id: BOX の分類ID（アドレスなら100番台）
    priority: 優先度
    """

    cur = conn.cursor()

    # 行頭のタプル (...) を抽出する正規表現
    tuple_re = re.compile(r"^\([^)]*\)")

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

            tuple_str = m.group(0)

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


conn = sqlite3.connect("db/ccgDB.sqlite")

register_pos_patterns_from_log(
    conn,
    filename="logall3.txt",  # あなたのログファイル
    lang=1,                    # 日本語
    class_id=100,              # アドレス句
    priority=1
)
