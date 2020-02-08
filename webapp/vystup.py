#!venv/bin/python 

import sys
import io
import os
import json
from urllib.parse import parse_qs
from clir_functions import CLIR

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

LIMIT = 200

C = CLIR('cs')

qs = parse_qs(os.environ['QUERY_STRING']) if 'QUERY_STRING' in os.environ else {}
if 'q' in qs:
    q = qs['q'][0]
    C.print_header(title = q + ' - ' + C.t('CLIR results') )
    C.print_h1(C.t('Results for query') + ' ' + q)
    results = C.get_results(q)    
    C.print_p('Number of results found: ' + str(results.numFound))
    for i, doc in enumerate(results.docs):
        docid = doc['id']
        print('<br>')
        print('Result', i+1, 'is document ID', docid, end='<br>')
        hl = results.hl[docid]
        if 'content' in hl:
            for item in hl['content']:
                print('...', item, '...', end='<br>')
        if 'content' in doc:
            sd = str(doc['content'])
        else:
            sd = str(doc)
        if len(sd) <= LIMIT:
            print(sd, end='<br>')
        else:
            print(sd[:LIMIT], '...', end='<br>')

    print('<hr>')
    print('<pre>')
    print(json.dumps(results.response.json(), indent=4))
    print('</pre>')
    print('<hr>')

else:
    C.print_header(title = 'CLIR: nebyl zadán žádný dotaz')
    C.print_h1('Nebyl zadán žádný dotaz')

C.print_footer()
