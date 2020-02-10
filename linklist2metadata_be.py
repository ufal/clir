#!/usr/bin/env python3
#coding: utf-8

import sys
import json
from trafo import translate

# tuned for nku_be at the moment

year = sys.argv[1]

def readnumfromfile(filename):
    with open(filename) as f:
        return int(f.read().rstrip())


with open('linklist.'+year+'.csv') as linklist:
    for line in linklist:
        url, name = line.rstrip().split('\t')
        pdffilename = url.split('/')[-1]
        metafilename = year + '/' + pdffilename[:-3] + 'meta'
        metadata = {
                'url': url,
                'name': name,
                'name_en': name,
                'pages': readnumfromfile(year + '/' + pdffilename + '.pages'),
                'words': readnumfromfile(year + '/' + pdffilename + '.words'),
                }
        # translate name to other langs
        if 'é' in name:
            srclang = 'fr'
            metadata['name_fr'] = name
            tgtlang = 'en'
            name_en = translate(name, srclang, tgtlang)
            if name_en:
                metadata['name_'+tgtlang] = name_en
                name = name_en
                srclang = 'en'
                for tgtlang in ['cs', 'de']:
                    name_tr = translate(name, srclang, tgtlang)
                    if name_tr:
                        metadata['name_'+tgtlang] = name_tr
        else:
            srclang = 'en'
            for tgtlang in ['cs', 'de', 'fr']:
                name_tr = translate(name, srclang, tgtlang)
                if name_tr:
                    metadata['name_'+tgtlang] = name_tr

        # output
        with open(metafilename, 'w') as metafile:
            json.dump(metadata, metafile, indent=4)


