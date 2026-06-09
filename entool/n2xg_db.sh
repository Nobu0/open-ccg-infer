date

: <<'COMMENT_OUT'
echo "この部分はコメントアウトされるため"
echo "実行されません"

sqlite3 db/ccgDB.sqlite "DELETE from box_tbl WHERE lang=2"
sqlite3 db/ccgDB.sqlite "DELETE from pos_box_tbl WHERE lang=2"
sqlite3 db/ccgDB.sqlite "DELETE from his_box_tbl WHERE lang=2"
sqlite3 db/ccgDB.sqlite "DELETE from ovlp_box_tbl WHERE lang=2"
#exit

#sqlite3 db/ccgDB.sqlite "SELECT * from pos_tbl LIMIT 5"

python entool/auto_box_en_x0x.py
COMMENT_OUT

sqlite3 db/ccgDB.sqlite "SELECT count(*) from box_tbl WHERE lang=2 ORDER BY class_id;"
sqlite3 db/ccgDB.sqlite "SELECT * from box_tbl WHERE lang=2 ORDER BY class_id LIMIT 10;"
sqlite3 db/ccgDB.sqlite "PRAGMA table_info(box_tbl);"
#exit

#python tool/load_pos_box.py
#python tool/batch_box.py
#python tool/view_box.py

#python tool/make_box.py
#python tool/his_box.py

sqlite3 db/ccgDB.sqlite "SELECT * from pos_box_tbl WHERE lang=2 LIMIT 10"
sqlite3 db/ccgDB.sqlite "SELECT * from box_tbl WHERE lang=2 LIMIT 10"
sqlite3 db/ccgDB.sqlite "SELECT class_id, COUNT(*) AS cnt
FROM box_tbl
WHERE lang = 2
GROUP BY class_id
ORDER BY class_id;
"
sqlite3 db/ccgDB.sqlite "SELECT * 
FROM box_tbl
WHERE lang = 2
GROUP BY class_id
ORDER BY class_id
LIMIT 10;
"
sqlite3 db/ccgDB.sqlite "SELECT * from his_box_tbl WHERE lang=2"
sqlite3 db/ccgDB.sqlite "SELECT * from ovlp_box_tbl WHERE lang=2"
echo "his_box_tbl count: "
sqlite3 db/ccgDB.sqlite "SELECT count(*) from his_box_tbl"
echo "ovlp_box_tbl count: "
sqlite3 db/ccgDB.sqlite "SELECT count(*) from ovlp_box_tbl"


sqlite3 db/ccgDB.sqlite "SELECT class_id, COUNT(*) AS cnt
FROM box_tbl
WHERE lang = 1
GROUP BY class_id
ORDER BY class_id;
"
sqlite3 db/ccgDB.sqlite "SELECT * 
FROM box_tbl
WHERE lang = 1
GROUP BY class_id
ORDER BY class_id
LIMIT 10;
"

date
exit
