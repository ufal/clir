#!/usr/bin/env python3
#coding: utf-8

import requests

class results:
    def __init__(self, response):
        self.response = response
        j = response.json()
        self.numFound = j['response']['numFound']
        self.docs = j['response']['docs']
        self.hl = j['highlighting']

class CLIR:

    texts = {
            'CLIR results': {'cs': 'výsledky CLIR',},
            'Results for query': {'cs': 'Výsledky pro dotaz',},
            
            
            }

    def __init__(self, language):
        self.language = language

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
            <style>
                em {font-weight: bold}
            </style>
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

    def print_p(self, text):
        print('<p>' + text + '</p>')

    def get_results(self, q):
        url = 'http://sol2:8989/solr/techproducts/select'
        data = {'q': q,
                'hl': 'true', # highlighting
                'hl.fl' : 'content', # what to highlight
                }
        # highlighting->id->content[0] ... <em> highlights search query
        response = requests.get(url, data = data)
        #response.encoding='utf8'
        return results(response)

