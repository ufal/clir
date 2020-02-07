#!/bin/bash

# This is to be run from the root, i.e. d starts with data/

set -o xtrace

d=$1 # the directory, e.g. data/data_fr/source_fr/nku_be/2012
s=$2 # source language, e.g. fr
t=$3 # target language, e.g. en

# $d must contain data_$s
# stores the translation into data/data_$t/...

L=50000

for f in $d/*.txt;
do
    if [ $(wc -w < $f) -lt $L ]
    then
        ./trafo.py $f $s $t > ${f/data_$s/data_$t}
    else
        echo File $f too large: $(wc -w < $f) words, limit is $L words
    fi
done

