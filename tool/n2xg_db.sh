date

sqlite3 db/ccgDB.sqlite "DELETE from box_tbl"
sqlite3 db/ccgDB.sqlite "DELETE from pos_box_tbl"
sqlite3 db/ccgDB.sqlite "DELETE from his_box_tbl"
sqlite3 db/ccgDB.sqlite "DELETE from ovlp_box_tbl"
exit

#sqlite3 db/ccgDB.sqlite "SELECT * from box_tbl"
#sqlite3 db/ccgDB.sqlite "SELECT * from pos_tbl LIMIT 5"

#python tool/load_pos_box.py
#python tool/batch_box.py
python tool/view_box.py

#python tool/make_box.py
#python tool/his_box.py

sqlite3 db/ccgDB.sqlite "SELECT * from pos_box_tbl LIMIT 10"
sqlite3 db/ccgDB.sqlite "SELECT * from box_tbl LIMIT 10"
sqlite3 db/ccgDB.sqlite "SELECT * from his_box_tbl"
sqlite3 db/ccgDB.sqlite "SELECT * from ovlp_box_tbl"

date
exit
