import sqlite3

DB = "db/ccgDB.sqlite"


conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS pos_box_tbl")

#　品詞テーブルから、BOX化するためのテーブル
cur.execute("""
CREATE TABLE pos_box_tbl (
    pat_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    lang       INTEGER,          -- 1:日本語, 2:英語
    pat_len    INTEGER,          -- パターン長
    pat_tags   TEXT,             -- "nns,vb,助動,格,vb,nnr"
    class_id   INTEGER,          -- BOX の分類
    priority   INTEGER,          -- 優先度
    note       TEXT              -- メモ
);
""")

cur.execute("DROP TABLE IF EXISTS ovlp_box_tbl")

cur.execute("""
CREATE TABLE IF NOT EXISTS ovlp_box_tbl (
    ov_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    act_id    INTEGER,
    box1_id   INTEGER,
    box2_id   INTEGER,
    overlap_w INTEGER,   -- 重なり幅
    ratio1    REAL,      -- box1 に対する重なり率
    ratio2    REAL,      -- box2 に対する重なり率
    updt      DATETIME DEFAULT (DATETIME('now', 'localtime'))
);
""")


cur.execute("DROP TABLE IF EXISTS his_box_tbl")

cur.execute("""
CREATE TABLE IF NOT EXISTS his_box_tbl (
    his_id     INTEGER PRIMARY KEY AUTOINCREMENT,  -- 履歴ID
    act_id     INTEGER NOT NULL,                   -- 法令ID
    name       TEXT,                               -- 概要（例：ADDR BOX 初期化）
    desc       TEXT,                               -- 関係した品詞の種類等
    lang       INTEGER NOT NULL,                   -- 言語
    all_pos    INTEGER,                            -- pos_tbl の生データ個数
    box_cnt    INTEGER,                            -- BOX の個数
    box_ave    REAL,                               -- BOX の平均幅
    box_hed    REAL,                               -- BOX の位置率（0〜100）
    box_ovlp   REAL,                               -- 重なり率        
    status     INTEGER DEFAULT 0,                  -- 処理ステータス
    updt       DATETIME DEFAULT (DATETIME('now', 'localtime')),
    cnt        INTEGER DEFAULT 0
);
""")

conn.commit()
conn.close()

print("[DB] Initialized.")

exit()


cur.execute("DROP TABLE IF EXISTS box_class_tbl")

cur.execute("""
CREATE TABLE IF NOT EXISTS box_class_tbl (
    class_id   INTEGER,               -- 細分類コード
    name       TEXT,                  -- 分類名
    desc       TEXT,                  -- 説明
    status     INTEGER DEFAULT 0,
    updt       DATETIME DEFAULT (DATETIME('now', 'localtime')),
    cnt        INTEGER DEFAULT 0
);
""")

cur.execute("""
INSERT INTO box_class_tbl (class_id, name, desc) VALUES
(101, 'ADDR_ART', '条（Article）'),
(102, 'ADDR_PAR', '項（Paragraph）'),
(103, 'ADDR_NUM', '号（Item Number）'),

(201, 'FIXED_PP', '英語の固定前置詞句（in accordance with など）'),
(202, 'FIXED_INF', '英語の不定詞句（in order to など）'),

(301, 'NP_SIMPLE', '名詞句（単純）'),
(302, 'NP_REL', '名詞句（連体修飾あり）'),
(303, 'NP_ADDR', 'アドレスを含む名詞句、数詞を含む'),
(304, 'NP_OTHER', 'その他の名詞句等'),

(401, 'CCG_LEFT', 'CCG 左結合（A/B + B → A）'),
(402, 'CCG_RIGHT', 'CCG 右結合（B + B\\A → A）'),

(501, 'PP', '前置詞句（英語）'),
(502, 'ADV', '副詞句'),
(503, 'CLAUSE', '節（S/NP, S\\NP など）');
""")


cur.execute("DROP TABLE IF EXISTS box_tbl")

cur.execute("""
CREATE TABLE IF NOT EXISTS box_tbl (
    box_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    act_id     INTEGER NOT NULL,
    lang       INTEGER NOT NULL,
    start_id   INTEGER NOT NULL,
    end_id     INTEGER NOT NULL,
    box_type   TEXT,
    class_id   INTEGER,
    ccg        TEXT,
    content    TEXT,
    status     INTEGER DEFAULT 0,
    updt       DATETIME DEFAULT (DATETIME('now', 'localtime')),
    cnt        INTEGER DEFAULT 0,
    UNIQUE (act_id, start_id, end_id, box_type)
);
""")



#-- 0. 形態素データ（pos_tbl）
cur.execute("DROP TABLE IF EXISTS pos_tbl")

cur.execute("""
CREATE TABLE IF NOT EXISTS pos_tbl (
    src_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    act_id      INTEGER NOT NULL,  -- act_tbl.id
    line_num    INTEGER,           -- 元ファイルの論理行
    word        TEXT,              -- 単語
    pos         TEXT,              -- 品詞
    lang        INTEGER,           -- 1:JP, 2:EN
    status      INTEGER,        
    updt        DATETIME DEFAULT (DATETIME('now', 'localtime')),
    cnt         INTEGER DEFAULT 0
    -- FOREIGN KEY (act_id) REFERENCES act_tbl(act_id)
);
""")

# -- 1. 法令プロジェクト管理（act_tbl）
# -- 全ての解析のルートとなるテーブル
cur.execute("DROP TABLE IF EXISTS act_tbl")

cur.execute("""
CREATE TABLE IF NOT EXISTS act_tbl (
    act_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    lang    INTEGER DEFAULT 1,     -- 1:JP, 2:EN, 3:JP-EN
    catg    INTEGER,               -- 1:憲法, 2:法律, 3:規則 等
    status  INTEGER DEFAULT 1,     -- 1:有効   
    title   TEXT NOT NULL,         -- 法令名称
    file    TEXT,                  -- ローカルファイル名
    vers    TEXT,                  -- バージョン（令和〇年改正等）
    url     TEXT,                  -- e-Gov等のソースURL
    insdat  DATETIME DEFAULT (DATETIME('now', 'localtime'))
);
""")


