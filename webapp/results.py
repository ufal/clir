#!/usr/bin/env python3

import sys
import io
from clir_functions import CLIR

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

C = CLIR()

if C.searchquery:
    C.print_header(title = C.searchquery + ' - ' + C.t('CLIR results') )
    print(C.h1(C.t('Results for query') + ' <em>' + C.searchquery + '</em>'))
    results = C.get_results()
    print(C.p(C.t('Number of results found') + ': ' + str(results.numFound), cl="header"))
    print('<hr>')
    C.show_results(results)
    #results.debugprint()
else:
    C.print_header(title = C.t('CLIR: no query was specified'))
    print(C.h1(C.t('CLIR: no query was specified')))

C.print_footer()
