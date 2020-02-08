#!/usr/bin/env python3
#coding: utf-8

import requests
import json

class Results:
    def __init__(self, response):
        self.response = response
        self.json = response.json()
        self.numFound = self.json['response']['numFound']
        
        docs = self.json['response']['docs']
        hl = self.json['highlighting']
        
        self.results = list()
        for i, doc in enumerate(docs):
            doc_hl = hl[doc['id']]
            self.results.append(Result(doc, doc_hl))

    def debugprint(self):
        print('<hr>')
        print('<pre>')
        print(json.dumps(self.json, indent=4))
        print('</pre>')
        print('<hr>')

class Result:
    def __init__(self, doc, doc_hl):
        self.doc = doc
        if 'content' in doc:
            self.content = doc['content'][0]
        else:
            self.content = str(doc)
        if 'content' in doc_hl:
            self.hl = doc_hl['content'][0]
        else:
            self.hl = None
        self.docid = doc['id']
        if '/data/' in self.docid:
            # this hopefully means it is a document with our special ID # strucure
            self.info = Result.parse_id(self.docid)
            self.metadata = Result.get_metadata(self.info)
        else:
            self.info = None
            self.metadata = None

    def parse_id(docid):
        # e.g. /data/data_cs/source_fr/nku_be/2020/2020_02_report.txt
        prefix = docid.find('/data/')
        assert prefix != -1
        parts = docid[prefix+1:].split('/', 6)
        assert len(parts) == 6
        # data
        assert parts[0] == 'data'
        info = {}
        # data_cs
        assert len(parts[1]) == 7 and parts[1].startswith('data_')
        info['lang'] = parts[1][-2:]
        # source_fr
        assert len(parts[2]) == 9 and parts[2].startswith('source_')
        info['src'] = parts[2][-2:]
        # nku_be
        assert len(parts[3]) == 6 and parts[3].startswith('nku_')
        info['nku'] = parts[3][-2:]
        # 2020
        assert len(parts[4]) == 4 and parts[4].isdecimal()
        info['year'] = int(parts[4])
        # 2020_02_report.txt
        assert parts[5].endswith('.txt')
        info['filename'] = parts[5][:-4]
        return info


    def get_metadata(info):
        return None


    def show(self, C):
        print('<div class="result" id="' + self.docid + '">')
        if self.metadata:
            C.print_h2(self.metadata['name'])
        elif self.info:
            C.print_h2(self.info['filename'])
        else:
            C.print_h2(self.docid)
        if self.hl:
            C.print_hl(self.hl)
        else:
            if len(self.content) < C.LIMIT:
                C.print_p(self.content)
            else:
                C.print_p(self.content[:C.LIMIT] + '...')
        print('</div>')

class CLIR:

    texts = {
            'CLIR results': {'cs': 'výsledky CLIR',},
            'Results for query': {'cs': 'Výsledky pro dotaz',},
            'Number of results found': {'cs': 'Počet nalezených výsledků',},
            'CLIR: no query was specified': {'cs': 'CLIR: nebyl zadán žádný dotaz',},
            '': {'cs': '',},
            '': {'cs': '',},
            '': {'cs': '',},
            
            
            }

    def __init__(self, language, url):
        self.language = language
        self.url = url
        self.LIMIT = 200

    def t(self, text):
        if text in CLIR.texts and self.language in CLIR.texts[text]:
            return CLIR.texts[text][self.language]
        else:
            return text

    def print_header(self, title='CLIR'):
        print('''Content-Type: text/html;charset=utf-8

        <html>
        <head>
            <title>''' + title + '''</title>
            <link rel="stylesheet" type="text/css" href="http://ufallab.ms.mff.cuni.cz/~rosa/elitr/clir.css">
        </head>

        <body>
        ''')

    def print_footer(self):
        print('''
        </body>        
        </html>        
        ''')

    def print_h1(self, text):
        print('<h1>' + text + '</h1>')

    def print_h2(self, text):
        print('<h2>' + text + '</h2>')

    def print_p(self, text):
        print('<p>' + text + '</p>')

    def print_hl(self, text):
        print('<div class="hl">' + text + '</div>')

    def get_results(self, q):
        data = {'q': q,
                'hl': 'true', # highlighting
                'hl.fl' : 'content', # what to highlight
                }
        # highlighting->id->content[0] ... <em> highlights search query
        response = requests.get(self.url, data = data)
        #response.encoding='utf8'
        return Results(response)

    def show_results(self, results):
        for result in results.results:
            result.show(self)


