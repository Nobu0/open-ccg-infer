#python tool/ccg_step2.py
python tool/ccg_graphviz.py
exit

#sqlite3 db/ccgDB.sqlite "UPDATE pos_tbl SET lang = 1 WHERE lang = 'jp';"
#sqlite3 db/ccgDB.sqlite "UPDATE pos_tbl SET lang = 2 WHERE lang = 'en';"

#sqlite3 db/ccgDB.sqlite "SELECT * FROM pos_tbl LIMIT 10"

#sqlite3 db/ccgDB.sqlite ".schema 'pos_tbl'"
#sqlite3 db/ccgDB.sqlite "SELECT * FROM box_tbl WHERE class_id=302 LIMIT 10"
#python tool/clean_box.py
#sqlite3 db/ccgDB.sqlite "SELECT * FROM box_tbl WHERE class_id=302 LIMIT 10"
#exit
#python tool/assign_ccg.py
sqlite3 db/ccgDB.sqlite "SELECT * FROM box_tbl WHERE act_id=1;"

exit
#sqlite3 db/ccgDB.sqlite "PRAGMA table_info(ccg_token_tbl);"
sqlite3 db/ccgDB.sqlite "SELECT COUNT(*) FROM ccg_token_tbl;"
echo ""
sqlite3 db/ccgDB.sqlite "
SELECT act_id, lang, COUNT(*) 
FROM ccg_token_tbl
GROUP BY act_id, lang;"
echo ""

sqlite3 db/ccgDB.sqlite "SELECT * FROM ccg_token_tbl WHERE act_id=1 LIMIT 20;"

sqlite3 db/ccgDB.sqlite "
SELECT b.start_id, b.end_id, p.src_id, p.word
FROM box_tbl b
LEFT JOIN pos_tbl p
  ON b.start_id = p.src_id
WHERE b.act_id = 1 AND b.lang = 1
LIMIT 20;
"

#python tool/ccg_step1.py
python tool/ccg_step2.py