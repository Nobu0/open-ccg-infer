
#stack run "inpen.txt"

date

echo "304-305 NX-4"
python entool/auto_gram_en_30x.py 4 > logenNX4.txt
wc logenNX4.txt

echo "304-305 NX-6"
python entool/auto_gram_en_30x.py 6 > logenNX6.txt
wc logenNX6.txt

date