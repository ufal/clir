#!/usr/bin/env python3
#coding: utf-8

import sys
import json

year = sys.argv[1]

with open('linklist.'+year+'.csv') as linklist:
    for line in linklist:
        url, name = line.rstrip().split('\t')
        pdffilename = url.split('/')[-1]
        metafilename = year + '/' + pdffilename[:-3] + 'meta'
        metadata = {
                'url': url,
                'name': name,
                }
        with open(metafilename, 'w') as metafile:
            json.dump(metadata, metafile)


