#!/bin/bash

# This is to be run from the root, i.e. d starts with data/

#set -o xtrace

d=$1 # the directory, e.g. data/data_fr/source_fr/nku_be/2012
s=$2 # source language, e.g. fr
t=$3 # target language, e.g. en

# $d must contain data_$s
# stores the translation into data/data_$t/...

L=50000

td=${d/data_$s/data_$t}
echo Translate files in $d from $s to $t, store into $td >&2
mkdir -p $td

for f in $d/*.txt;
do
    echo >&2
    if [ -s $f ]
    then
        if [ $(wc -w < $f) -lt $L ]
        then
            echo Translate file $f: $(wc -w < $f) words, $(wc -l < $f) lines, $(wc -m < $f) characters >&2
            ./trafo.py $f $s $t > ${f/data_$s/data_$t}
            echo Done: $(ls $td/*.txt | wc -l) / $(ls $d/*.txt | wc -l) >&2
        else
            echo File $f too large: $(wc -w < $f) words, limit is $L words >&2
        fi
     fi
done

