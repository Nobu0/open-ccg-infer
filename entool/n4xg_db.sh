
: <<'COMMENT_OUT'


sqlite3 db/ccgDB.sqlite "DELETE FROM box_tbl WHERE class_id=900 AND lang=2;"
sqlite3 db/ccgDB.sqlite "DELETE FROM box_tbl WHERE class_id=901 AND lang=2;"

python entool/auto_box_90x.py

sqlite3 db/ccgDB.sqlite "SELECT count(*) FROM box_tbl WHERE class_id>800 AND lang=2;"

COMMENT_OUT

#sqlite3 db/ccgDB.sqlite "SELECT DISTINCT class_id, box_type FROM box_tbl WHERE class_id < 899 AND lang=2 ORDER BY class_id, box_type;"

#sqlite3 db/ccgDB.sqlite "SELECT printf('data(%d, \"%s\").', u.class_id, u.box_type) FROM (SELECT DISTINCT class_id, box_type FROM box_tbl WHERE class_id < 899 AND lang=2) AS u ORDER BY u.class_id, u.box_type;"

python entool/get_not_box.py

#python entool/sorted_pos.py > output_pos.txt
