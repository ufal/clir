#!venv/bin/python 

import sys
from clir_functions import CLIR, Document

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

C = CLIR()

docid = CLIR.qs2p(C.qs, 'docid')

if docid:
    document = Document(docid)

    if document.info:
        name = document.getname(lang)
        C.print_header(title = name)
        print(C.h1(name))
        if CLIR.searchquery:
            print(C.p('{}: {}'.format(
                C.t('Highlighted for query'), C.searchquery), cl="header"))

    else:
        C.print_header(title = C.t('CLIR: cannot display document'))
        print(C.h1(C.t('CLIR: cannot display document')))
else:
    C.print_header(title = C.t('CLIR: no document was specified'))
    print(C.h1(C.t('CLIR: no document was specified')))

print('</body></html>')

