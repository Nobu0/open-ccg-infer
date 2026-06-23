

#sqlite3 db/ccgDB.sqlite "DELETE FROM box_tbl WHERE class_id=900 AND lang=2;"
#sqlite3 db/ccgDB.sqlite "DELETE FROM box_tbl WHERE class_id=901 AND lang=2;"

#python entool/auto_box_90x.py

python entool/get_not_box.py

#python entool/sorted_pos.py > output_pos.txt
