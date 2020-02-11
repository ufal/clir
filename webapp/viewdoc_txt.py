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
        C.print_header(title = name, nobody=True)
        print('<body>')
        document.show_parallel(C)
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
