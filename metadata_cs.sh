#!/bin/bash

for f in $1/*.pdf
do
    f=${f%.pdf}
    pdfinfo $f.pdf|grep Pages|grep -o '[0-9]*' > $f.pages
    wc -w < $f.txt > $f.words
done
    
/home/rosa/elitr/clir/linklist2metadata_cs.py $1

rm $1/*.words $1/*.pages
