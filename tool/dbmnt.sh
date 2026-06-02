
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
