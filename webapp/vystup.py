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

C = CLIR(language = lang, url = 'http://sol2:8989/solr/techproducts/select')

if 'q' in qs:
    q = qs['q'][0]
    C.searchquery = q
    C.print_header(title = q + ' - ' + C.t('CLIR results') )
    print(C.h1(C.t('Results for query') + ' <em>' + q + '</em>'))
    results = C.get_results(q)    
    print(C.p(C.t('Number of results found') + ': ' + str(results.numFound)))
    print('<hr>')
    C.show_results(results)
    #results.debugprint()
else:
    C.print_header(title = C.t('CLIR: no query was specified'))
    print(C.h1(C.t('CLIR: no query was specified')))

C.print_footer()
