#!/usr/bin/env python3

import sys
import io
from clir_functions import CLIR, Document

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

C = CLIR()
C.print_header(nobody=True)
C.print_footer(nohr=True)
