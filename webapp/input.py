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

C.print_header(title = C.t('CLIR query') )
print(C.h1(C.t('CLIR query')))
print('<hr>')
C.print_searchform()
C.print_footer()
