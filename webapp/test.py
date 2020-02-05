#!venv/bin/python 

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Content-Type: text/plain;charset=utf-8")
print("")

from urllib.parse import parse_qs
import os
#print(os.environ['QUERY_STRING'])
#print(parse_qs(os.environ['QUERY_STRING']))

qs = parse_qs(os.environ['QUERY_STRING'])
if 'q' in qs:
    q = qs['q'][0]
    print('Query:', q)
else:
    print('No query')

print("Done.")

