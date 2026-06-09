date


#sqlite3 db/ccgDB.sqlite ".schema 'box_tbl'"
#sqlite3 db/ccgDB.sqlite "DELETE FROM pos_box_tbl WHERE class_id=301 AND lang=2;"
#sqlite3 db/ccgDB.sqlite "DELETE FROM box_tbl WHERE class_id=301 AND lang=2;"
#sqlite3 db/ccgDB.sqlite "DELETE FROM his_box_tbl WHERE lang=2;"
#exit

sqlite3 db/ccgDB.sqlite "SELECT count(*) from box_tbl WHERE lang=2;"
sqlite3 db/ccgDB.sqlite "SELECT * from pos_tbl LIMIT 5"

echo "load_pos_bos.py"
python entool/load_pos_box.py

echo "pos_box_tbl count: "
sqlite3 db/ccgDB.sqlite "SELECT count(*) from pos_box_tbl WHERE class_id=302 AND lang=2;"
sqlite3 db/ccgDB.sqlite "SELECT * from pos_box_tbl WHERE class_id=302 AND lang=2 LIMIT 10;"

echo "batch_box.py"
python entool/batch_box.py 301
#python entool/batch_box.py 302
#python entool/batch_box.py 303
#python entool/batch_box.py 304

echo "box_tbl count: "
sqlite3 db/ccgDB.sqlite "SELECT count(*) from box_tbl WHERE lang=2;"
sqlite3 db/ccgDB.sqlite "SELECT * from box_tbl WHERE lang=2 LIMIT 10"

echo "his_box_tbl count: "
sqlite3 db/ccgDB.sqlite "SELECT count(*) from his_box_tbl WHERE lang=2;"
echo "ovlp_box_tbl count: "
sqlite3 db/ccgDB.sqlite "SELECT count(*) from ovlp_box_tbl WHERE lang=2;"


date
exit

