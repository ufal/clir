#!venv/bin/python 

import sys
from clir_functions import CLIR

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

C = CLIR()

C.print_header(title = C.t('CLIR query') )
print(C.h1(C.t('CLIR query')))
print('<hr>')

C.print_searchform()

C.print_footer()
