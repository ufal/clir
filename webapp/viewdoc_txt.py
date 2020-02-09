#!venv/bin/python 

import sys
import io
import os
from urllib.parse import parse_qs
from clir_functions import CLIR, Document

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

qstring = os.environ['QUERY_STRING'] if 'QUERY_STRING' in os.environ else ''
qs = parse_qs(qstring)

if 'lang' in qs:
    lang = qs['lang'][0]
else:
    lang = 'en'

if 'q' in qs:
    q = qs['q'][0]
else:
    q = None

C = CLIR(language = lang, url = 'http://sol2:8989/solr/techproducts/select')

if 'docid' in qs:
    docid = qs['docid'][0]
    document = Document(docid)

    if document.info:
        name = document.getname(lang)
        C.print_header(title = name, nobody=True)
        print('<body>')
        document.show_parallel(C, q)
        print('</body></html>')
    else:
        # TODO this may be too harsh; even if we don't have metadata, we might
        # still have the document; but let's ignore that for now
        C.print_header(title = C.t('CLIR: cannot display document'))
        print(C.h1(C.t('CLIR: cannot display document')))
        C.print_footer()
else:
    C.print_header(title = C.t('CLIR: no document was specified'))
    print(C.h1(C.t('CLIR: no document was specified')))
    C.print_footer()
