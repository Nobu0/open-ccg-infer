sqlite3 db/ccgDB.sqlite "
CREATE TABLE ccg_tree_tbl (
    tree_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    act_id      INTEGER,
    lang        INTEGER,
    node_id     INTEGER,       -- ノード番号（1,2,3,...）
    parent_id   INTEGER,       -- 親ノード（NULL = root）
    label       TEXT,          -- CCG カテゴリ (NP, NP/NP)
    word        TEXT,          -- ノードの語（結合後の語も含む）
    start_id    INTEGER,       -- 元の開始 token ID
    end_id      INTEGER,       -- 元の終了 token ID
    created_at  TEXT DEFAULT CURRENT_TIMESTAMP
);
"

exit
sqlite3 db/ccgDB.sqlite "
CREATE TABLE ccg_log_tbl (
    log_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    act_id     INTEGER,
    lang       INTEGER,
    step_no    INTEGER,      -- 1,2,3,... の縮約ステップ番号
    left_cat   TEXT,         -- 左のカテゴリ (NP/NP)
    left_word  TEXT,         -- 左の語
    right_cat  TEXT,         -- 右のカテゴリ (NP)
    right_word TEXT,         -- 右の語
    result_cat TEXT,         -- 結果カテゴリ (NP)
    result_word TEXT,        -- 結果語
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"
exit

sqlite3 db/ccgDB.sqlite "CREATE INDEX idx_pos_act_line ON pos_tbl(act_id, line_num);"
sqlite3 db/ccgDB.sqlite "CREATE INDEX idx_pos_lang ON pos_tbl(lang);"

#sqlite3 db/ccgDB.sqlite "DELETE from pos_tbl"
sqlite3 db/ccgDB.sqlite "SELECT count(*) from pos_tbl"
#sqlite3 db/ccgDB.sqlite "SELECT * from pos_tbl LIMIT 100"

#exit

python tool/ddl_mnt.py

sqlite3 db/ccgDB.sqlite "SELECT * from box_class_tbl"

#python tool/pos_import.py

sqlite3 db/ccgDB.sqlite "SELECT count(*) from pos_tbl"
#sqlite3 db/ccgDB.sqlite "SELECT * from pos_tbl LIMIT 100"
