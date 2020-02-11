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
        name = document.getname(C.language)
        C.print_header(title = name, nobody=True)

        pdf_url = document.get_source_pdf(C.staticurl)

        print('''<frameset cols="50%, *">
            <frame src="viewdoc_txt.py?''' + C.qstring + '''">
            <frame src="''' + pdf_url + '''">
        </frameset></html>''')

    else:
        C.print_header(title = C.t('CLIR: cannot display document'), nobody=True)
        print(C.h1(C.t('CLIR: cannot display document')))
        print('</body></html>')
else:
    C.print_header(title = C.t('CLIR: no document was specified'))
    print(C.h1(C.t('CLIR: no document was specified')))
    print('</body></html>')
