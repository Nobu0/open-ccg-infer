
#python entool/view_box.py
#sqlite3 db/ccgDB.sqlite "SELECT * from ccg_tree_tbl WHERE lang=2"
#exit

echo "ccg_tree_tbl count"
sqlite3 db/ccgDB.sqlite "SELECT count(*) from ccg_tree_tbl WHERE lang=2"

python entool/ccg_assign.py
python entool/ccg_graphviz.py

#exit

#sqlite3 db/ccgDB.sqlite "DELETE FROM his_box_tbl WHERE his_id < 19"
#exit
#python tool/make_box.py
#python tool/his_box.py
sqlite3 db/ccgDB.sqlite ".schema 'box_tbl'"

sqlite3 db/ccgDB.sqlite "SELECT distinct class_id from box_tbl WHERE lang=2 ORDER BY class_id;"

echo "pos_box_tbl: count(*)"
sqlite3 db/ccgDB.sqlite "SELECT count(*) from pos_box_tbl WHERE lang=2"
sqlite3 db/ccgDB.sqlite "SELECT count(*) from pos_box_tbl WHERE lang=2 LIMIT 5"
echo "box_tbl class_id: 10x"
sqlite3 db/ccgDB.sqlite "SELECT count(*) from box_tbl WHERE class_id < 109 AND lang=2 ;"
sqlite3 db/ccgDB.sqlite "SELECT * from box_tbl WHERE class_id< 109 AND lang=2 ORDER BY box_id LIMIT 10 ;"
echo "box_tbl class_id: 20x"
sqlite3 db/ccgDB.sqlite "SELECT count(*) from box_tbl WHERE class_id=201 AND lang=2 ;"
sqlite3 db/ccgDB.sqlite "SELECT * from box_tbl WHERE class_id=201 AND lang=2 ORDER BY box_id LIMIT 10 ;"
echo "box_tbl class_id: 301"
sqlite3 db/ccgDB.sqlite "SELECT count(*) from box_tbl WHERE class_id=301 AND lang=2 ;"
sqlite3 db/ccgDB.sqlite "SELECT * from box_tbl WHERE class_id=301 AND lang=2 ORDER BY box_id LIMIT 10 ;"
echo "box_tbl class_id: 302"
sqlite3 db/ccgDB.sqlite "SELECT count(*) from box_tbl WHERE class_id=302 AND lang=2"
sqlite3 db/ccgDB.sqlite "SELECT * from box_tbl WHERE class_id=302 AND lang=2 ORDER BY box_id LIMIT 5 ;"
echo "box_tbl class_id: 303"
sqlite3 db/ccgDB.sqlite "SELECT count(*) from box_tbl WHERE class_id=303 AND lang=2"
sqlite3 db/ccgDB.sqlite "SELECT * from box_tbl WHERE class_id=303 AND lang=2 ORDER BY box_id LIMIT 5 ;"
echo "box_tbl class_id: 304"
sqlite3 db/ccgDB.sqlite "SELECT count(*) from box_tbl WHERE class_id=304 AND lang=2"
sqlite3 db/ccgDB.sqlite "SELECT * from box_tbl WHERE class_id=304 AND lang=2 ORDER BY box_id LIMIT 5 ;"
echo "box_tbl class_id: 305"
sqlite3 db/ccgDB.sqlite "SELECT count(*) from box_tbl WHERE class_id=305 AND lang=2"
sqlite3 db/ccgDB.sqlite "SELECT * from box_tbl WHERE class_id=305 AND lang=2 ORDER BY box_id LIMIT 5 ;"
echo "his_box_tbl"
sqlite3 db/ccgDB.sqlite "SELECT * from his_box_tbl"
echo "ovlp_box_tbl"
sqlite3 db/ccgDB.sqlite "SELECT * from ovlp_box_tbl"