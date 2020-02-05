#!venv/bin/python 

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

#print("Content-Type: text/plain;charset=utf-8")
print("Content-Type: text/html;charset=utf-8")
print("")

from urllib.parse import parse_qs
import os
#print(os.environ['QUERY_STRING'])
#print(parse_qs(os.environ['QUERY_STRING']))

import json
import requests

LIMIT = 200

print('''<style>
em {font-weight: bold}
</style>''')

qs = parse_qs(os.environ['QUERY_STRING'])
if 'q' in qs:
    q = qs['q'][0]
    print('Query:', q, end='<br>')

    url = 'http://sol2:8989/solr/techproducts/select'
    data = {'q': q,
            'hl': 'true', # highlighting
            'hl.fl' : 'content', # what to highlight
            }
    # highlighting->id->content[0] ... <em> highlights search query
    response = requests.get(url, data = data)
    #response.encoding='utf8'
    j = response.json()
    
    numFound = j['response']['numFound']
    docs = j['response']['docs']
    
    #print(j)
    print('Number of results found:', numFound, end='<br>')
    for i, doc in enumerate(docs):
        docid = doc['id']
        print('<br>')
        print('Result', i+1, 'is document ID', docid, end='<br>')
        hl = j['highlighting'][docid]
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
    print(json.dumps(j, indent=4))
    print('</pre>')
    print('<hr>')

else:
    print('No query', end='<br>')

print("Done.", end='<br>')

