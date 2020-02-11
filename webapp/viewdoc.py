#!/usr/bin/env python3

import sys
import io
from clir_functions import CLIR, Document

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

C = CLIR()

docid = CLIR.qs2p(C.qs, 'docid')

if docid:
    document = Document(docid)

    if document.info:
        name = document.getname(lang)
        C.print_header(title = name, nobody=True)

        print('''<frameset rows="120, *, 35">
            <frame src="viewdoc_header.py?''' + C.qstring + '''">
            <frame src="viewdoc_main.py?''' + C.qstring + '''">
            <frame src="viewdoc_footer.py">
        </frameset></html>''')

    else:
        C.print_header(title = C.t('CLIR: cannot display document'))
        print(C.h1(C.t('CLIR: cannot display document')))
        C.print_footer()
else:
    C.print_header(title = C.t('CLIR: no document was specified'))
    print(C.h1(C.t('CLIR: no document was specified')))
    C.print_footer()
