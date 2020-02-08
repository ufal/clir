#!/bin/bash

for f in $1/*.pdf
do
    pdfinfo $f|grep Pages|grep -o '[0-9]*' > $f.pages
    wc -w < ${f/pdf/txt} > $f.words
done
    
/home/rosa/elitr/clir/linklist2metadata.py $1

rm $1/*.words $1/*.pages
