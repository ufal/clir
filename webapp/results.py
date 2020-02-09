#!venv/bin/python 

import sys
import io
import os
from urllib.parse import parse_qs
from clir_functions import CLIR

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

qs = parse_qs(os.environ['QUERY_STRING']) if 'QUERY_STRING' in os.environ else {}

if 'lang' in qs:
    lang = qs['lang'][0]
else:
    lang = 'en'

if 'host' in qs:
    host =  qs['host'][0]
else:
    host = 'sol2'

if 'port' in qs:
    port =  qs['port'][0]
else:
    port = '8971'

if 'collection' in qs:
    collection =  qs['collection'][0]
else:
    collection = 'eurosaiall'


C = CLIR(language = lang, host = host, port = port, collection = collection)

if 'q' in qs:
    q = qs['q'][0]
    C.searchquery = q
    C.print_header(title = q + ' - ' + C.t('CLIR results') )
    print(C.h1(C.t('Results for query') + ' <em>' + q + '</em>'))
    results = C.get_results(q)    
    print(C.p(C.t('Number of results found') + ': ' + str(results.numFound), cl="header"))
    print('<hr>')
    C.show_results(results)
    #results.debugprint()
else:
    C.print_header(title = C.t('CLIR: no query was specified'))
    print(C.h1(C.t('CLIR: no query was specified')))

C.print_footer()
