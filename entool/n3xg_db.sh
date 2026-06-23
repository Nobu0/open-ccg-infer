date

: <<'COMMENT_OUT'
#sqlite3 db/ccgDB.sqlite ".schema 'box_tbl'"
sqlite3 db/ccgDB.sqlite "DELETE FROM box_tbl WHERE class_id=403 AND lang=2;"
sqlite3 db/ccgDB.sqlite "DELETE FROM box_tbl WHERE class_id=501 AND lang=2;"
sqlite3 db/ccgDB.sqlite "DELETE FROM box_tbl WHERE class_id=502 AND lang=2;"
sqlite3 db/ccgDB.sqlite "DELETE FROM box_tbl WHERE class_id=503 AND lang=2;"
#sqlite3 db/ccgDB.sqlite "DELETE FROM his_box_tbl WHERE lang=2;"
#exit

COMMENT_OUT

python entool/auto_box_vp_etc.py logenVP4.txt

# 配列の定義
list=(403 501 502 503)

# 配列の全要素でループ
for item in "${list[@]}"; do
    echo "No: $item"
    echo "pos_box_tbl count: class_id=$item"
    sqlite3 db/ccgDB.sqlite "SELECT count(*) from box_tbl WHERE class_id=$item AND lang=2;"
    sqlite3 db/ccgDB.sqlite "SELECT * from box_tbl WHERE class_id=$item AND lang=2 LIMIT 10;"
done

date
exit

