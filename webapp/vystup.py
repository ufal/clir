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

import json
import requests

LIMIT = 100

qs = parse_qs(os.environ['QUERY_STRING'])
if 'q' in qs:
    q = qs['q'][0]
    print('Query:', q)

    url = 'http://sol2:8989/solr/techproducts/select'
    data = {'q': q}
    response = requests.get(url, data = data)
    #response.encoding='utf8'
    j = response.json()
    
    numFound = j['response']['numFound']
    docs = j['response']['docs']
    
    #print(j)
    print('Number of results found:', numFound)
    for i, doc in enumerate(docs):
        print('Result', i+1, 'is document ID', doc['id'])
        sd = str(doc)
        if len(sd) <= LIMIT:
            print(sd)
        else:
            print(sd[:LIMIT], '...')

else:
    print('No query')

print("Done.")

