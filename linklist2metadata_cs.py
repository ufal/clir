#!/usr/bin/env python3
#coding: utf-8

import sys
import json
from trafo import translate
import os.path
from os import path

year = sys.argv[1]

def readnumfromfile(filename):
    with open(filename) as f:
        return int(f.read().rstrip())


with open('namelist.csv') as linklist:
    for line in linklist:
        filename, name = line.rstrip().split('\t')
        if filename[1:3] == year[-2:]:
            txtfilename = year + '/' + filename + '.txt'
            metafilename = year + '/' + filename + '.meta'
            print(year + '/' + filename)
            if path.exists(txtfilename) and not path.exists(metafilename):
                print('is go')
                metadata = {
                        'name': name,
                        'pages': readnumfromfile(year + '/' + filename + '.pages'),
                        'words': readnumfromfile(year + '/' + filename + '.words'),
                        }
                # translate name to other langs
                metadata['name_cs'] = name
                name_en = translate(name, 'cs', 'en')
                if name_en:
                    metadata['name_en'] = name_en
                    for tgtlang in ['fr', 'de']:
                        name_tr = translate(name_en, 'en', tgtlang)
                        if name_tr:
                            metadata['name_'+tgtlang] = name_tr

                # output
                with open(metafilename, 'w') as metafile:
                    json.dump(metadata, metafile, indent=4)


