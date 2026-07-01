# pos_tblとbox_tblでprologにデータを渡し、CCG解析をおこなう。

act_id=1
tmp_file=prolog/tbl_inf.pl
rm $tmp_file

echo ":- module(tbl_inf, [
    pos_tbl/4,       % 外部から呼び出せる述語
    box_tbl/4       % 外部から呼び出せる述語
])." > $tmp_file 

sqlite3 db/ccgDB.sqlite "
SELECT printf('pos_tbl(%d, %d, \"%s\", \"%s\").', u.src_id, u.line_num, u.pos, u.word) 
FROM (SELECT src_id, line_num, pos, word FROM pos_tbl WHERE act_id=${act_id} AND lang=2)
 AS u ORDER BY u.src_id;
" >> $tmp_file

sqlite3 db/ccgDB.sqlite "
SELECT printf('box_tbl(%d, %d, %d, \"%s\").', u.class_id, u.start_id, u.end_id, u.box_type) 
FROM (SELECT box_id, class_id, box_type, start_id, end_id FROM box_tbl WHERE act_id=${act_id} AND class_id < 899 AND lang=2)
 AS u ORDER BY u.start_id, u.end_id;
" >> $tmp_file

cat $tmp_file