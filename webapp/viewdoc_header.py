#!venv/bin/python 

import sys
import io
import os
from urllib.parse import parse_qs
from clir_functions import CLIR, Document

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

qs = parse_qs(os.environ['QUERY_STRING']) if 'QUERY_STRING' in os.environ else {}

if 'lang' in qs:
    lang = qs['lang'][0]
else:
    lang = 'en'

C = CLIR(language = lang, url = 'http://sol2:8989/solr/techproducts/select')

if 'docid' in qs:
    docid = qs['docid'][0]
    q = qs['q'][0] if 'q' in qs else None
    document = Document(docid)

    if document.metadata:
        name = document.getname(lang)
        C.print_header(title = name)
        print(C.h1(name))
        if q:
            print(C.p('{}: {}'.format(
                C.t('Highlighted for query'), q), cl="header"))

    else:
        # TODO this may be too harsh; even if we don't have metadata, we might
        # still have the document; but let's ignore that for now
        C.print_header(title = C.t('CLIR: cannot display document'))
        print(C.h1(C.t('CLIR: cannot display document')))
else:
    C.print_header(title = C.t('CLIR: no document was specified'))
    print(C.h1(C.t('CLIR: no document was specified')))

print('</body></html>')

