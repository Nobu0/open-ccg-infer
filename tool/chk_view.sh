
python tool/view_box.py

sqlite3 db/ccgDB.sqlite "DELETE FROM his_box_tbl WHERE his_id < 19"
#exit
#python tool/make_box.py
#python tool/his_box.py
echo "pos_box_tbl: count(*)"
sqlite3 db/ccgDB.sqlite "SELECT count(*) from pos_box_tbl"
sqlite3 db/ccgDB.sqlite "SELECT count(*) from pos_box_tbl LIMIT 5"
echo "box_tbl class_id: 301"
sqlite3 db/ccgDB.sqlite "SELECT count(*) from box_tbl WHERE class_id=301"
sqlite3 db/ccgDB.sqlite "SELECT * from box_tbl WHERE class_id=301 ORDER BY box_id LIMIT 10 ;"
echo "box_tbl class_id: 302"
sqlite3 db/ccgDB.sqlite "SELECT count(*) from box_tbl WHERE class_id=302"
sqlite3 db/ccgDB.sqlite "SELECT * from box_tbl WHERE class_id=302 ORDER BY box_id LIMIT 5 ;"
echo "box_tbl class_id: 303"
sqlite3 db/ccgDB.sqlite "SELECT count(*) from box_tbl WHERE class_id=303"
sqlite3 db/ccgDB.sqlite "SELECT * from box_tbl WHERE class_id=303 ORDER BY box_id LIMIT 5 ;"
echo "box_tbl class_id: 304"
sqlite3 db/ccgDB.sqlite "SELECT count(*) from box_tbl WHERE class_id=304"
sqlite3 db/ccgDB.sqlite "SELECT * from box_tbl WHERE class_id=304 ORDER BY box_id LIMIT 5 ;"
echo "his_box_tbl"
sqlite3 db/ccgDB.sqlite "SELECT * from his_box_tbl"
echo "ovlp_box_tbl"
sqlite3 db/ccgDB.sqlite "SELECT * from ovlp_box_tbl"