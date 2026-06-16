
#stack run "inpen.txt"

date

: <<'COMMENT_OUT'
echo "304-305 NX-4"
python entool/auto_gram_en_30x.py 4 > logenNX4.txt
wc logenNX4.txt

echo "304-305 NX-6"
python entool/auto_gram_en_30x.py 6 > logenNX6.txt
wc logenNX6.txt
COMMENT_OUT

python entool/auto_gram_vp.py 6 > logenVP6.txt

date