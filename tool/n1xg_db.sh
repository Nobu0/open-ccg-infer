date


#sqlite3 db/ccgDB.sqlite ".schema 'box_tbl'"
sqlite3 db/ccgDB.sqlite "DELETE FROM pos_box_tbl WHERE class_id=301;"
sqlite3 db/ccgDB.sqlite "DELETE FROM box_tbl WHERE class_id=301;"
#sqlite3 db/ccgDB.sqlite "DELETE FROM his_box_tbl"
#exit

sqlite3 db/ccgDB.sqlite "SELECT count(*) from box_tbl"
sqlite3 db/ccgDB.sqlite "SELECT * from pos_tbl LIMIT 5"
echo "load_pos_bos.py"
python tool/load_pos_box.py

echo "pos_box_tbl count: "
sqlite3 db/ccgDB.sqlite "SELECT count(*) from pos_box_tbl WHERE class_id=302;"
sqlite3 db/ccgDB.sqlite "SELECT * from pos_box_tbl WHERE class_id=302 LIMIT 10"

echo "batch_box.py"
python tool/batch_box.py 301
#python tool/batch_box.py 302
#python tool/batch_box.py 303
#python tool/batch_box.py 304

echo "box_tbl count: "
sqlite3 db/ccgDB.sqlite "SELECT count(*) from box_tbl"
sqlite3 db/ccgDB.sqlite "SELECT * from box_tbl LIMIT 10"

#echo "view_box.py "
#python tool/view_box.py

echo "his_box_tbl count: "
sqlite3 db/ccgDB.sqlite "SELECT count(*) from his_box_tbl"
echo "ovlp_box_tbl count: "
sqlite3 db/ccgDB.sqlite "SELECT count(*) from ovlp_box_tbl"

####python tool/make_box.py
####python tool/his_box.py

#sqlite3 db/ccgDB.sqlite "SELECT * from pos_box_tbl LIMIT 10"
#sqlite3 db/ccgDB.sqlite "SELECT * from box_tbl LIMIT 10"
#sqlite3 db/ccgDB.sqlite "SELECT * from his_box_tbl"
#sqlite3 db/ccgDB.sqlite "SELECT * from ovlp_box_tbl"

date
exit

sqlite3 db/ccgDB.sqlite """
SELECT src_id
FROM pos_tbl
WHERE word REGEXP '第[一二三四五六七八九十百千0-9]+(条|項|号)';
"""

exit

sqlite3 db/ccgDB.sqlite """
SELECT 
    a.src_id AS id1,
    b.src_id AS id2,
    c.src_id AS id3,
    a.word, b.word, c.word
FROM pos_tbl a
JOIN pos_tbl b ON b.src_id = a.src_id + 1
JOIN pos_tbl c ON c.src_id = a.src_id + 2
WHERE a.act_id = 1;
"""


