#!/usr/bin/env python3
#coding: utf-8

import requests
import json
from clir_texts import CLIRtexts

import logging
#logging.basicConfig(
#    format='%(asctime)s %(message)s',
#    datefmt='%Y-%m-%d %H:%M:%S',
#    level=logging.INFO)

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

class Document:
    def __init__(self, docid):
        self.docid = docid
        if '/data/' in self.docid:
            # this hopefully means it is a document with our special ID strucure
            self.parse_id()     # fills in self.info
            self.get_metadata()     # fills in self.metadata
        else:
            self.info = None
            self.metadata = None

    def parse_id(self):
        self.info = Document._parse_id(self.docid)
    
    def _parse_id(docid):
        # e.g. /data/data_cs/source_fr/nku_be/2020/2020_02_report.txt
        prefix = docid.find('/data/')
        assert prefix != -1
        
        datapath = docid[prefix:]
        parts = datapath[1:].split('/', 6)
        assert len(parts) == 6, parts
        
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
        
        info['datapath'] = datapath
        info['srcdir'] = '/'.join([
            '',
            'data',
            'data_' + info['src'],
            'source_' + info['src'],
            'nku_' + info['nku'],
            str(info['year'])
            ])
        
        return info


    def get_metadata(self):
        self.metadata = Document._get_metadata(self.info)

    def _get_metadata(info):
        metadata = {}
        try:
            metafilename = '.' + info['srcdir'] + '/' + info['filename'] + '.meta'
            with open(metafilename) as metafile:
                metadata = json.load(metafile)
                return metadata
        except:
            logging.warn('Cannot open {}'.format(metafilename))
            return None

    def getname(self, lang='en'):
        name = self.docid
        if self.metadata:
            lkey = 'name_' + lang
            if lkey in self.metadata:
                name = self.metadata[lkey]
            else:
                name = self.metadata['name']
        elif self.info:
            name = self.info['filename']
        return name

    # use C.URLPREFIX to get http url
    def get_source_txt(self, urlprefix = ''):
        return urlprefix + self.info['srcdir'] + '/' + self.info['filename'] + '.txt'
    
    def get_source_pdf(self, urlprefix = ''):
        return urlprefix + self.info['srcdir'] + '/' + self.info['filename'] + '.pdf'

    def show_parallel(self, C):
        trfilename  = '.' + self.info['datapath']
        srcfilename = '.' + self.get_source_txt()
        
        
        print('<table style="width: 100%">')
        print('<tr><th>Translation</th><th>Original</th></tr>')
        print('</table>')

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

        self.document = Document(self.docid)
        self.info = self.document.info
        self.metadata = self.document.metadata


    # especially for Czech;
    # 1 -> '',
    # 2-4 -> 's2',
    # >4 -> 's'
    def pluralsuffix(number):
        suffix = 's'
        if number == 1:
            suffix = ''
        if 1 < number < 5:
            suffix = 's2'
        return suffix

    def show(self, C):
        print('<div class="result" id="' + self.docid + '">')
        
        if self.info:
            # year and SAI
            info_sai_year = '{}, {}'.format(
                C.t('nku_' + self.info['nku']),
                str(self.info['year'])
                )
        
            # language and pages and words
            if self.metadata:
                info_lang_p_w = '{}, {} {}, {} {}'.format(
                    C.t(self.info['src']),
                    self.metadata['pages'],
                    C.t('page' + Result.pluralsuffix(self.metadata['pages'])),
                    self.metadata['words'],
                    C.t('word' + Result.pluralsuffix(self.metadata['words'])),
                    )
            else:
                info_lang_p_w = C.t(self.info['src'])
            
            print(C.details(
                C.div(info_sai_year) + 
                C.div(info_lang_p_w)
                ))
                
        # document name
        name = self.document.getname(C.language)
        print(C.h2(name))
        
        # search results highlight
        if self.hl:
            print(C.hl(self.hl))
        else:
            if len(self.content) < C.LIMIT:
                print(C.p(self.content))
            else:
                print(C.p(self.content[:C.LIMIT] + '...'))
        
        # document info
        if self.info:
            print('<div>')
        
            # Preview link
            previewurl = 'viewdoc.py?lang={}&amp;docid={}&amp;q={}'.format(
                    C.language, self.info['datapath'], C.searchquery)
            print(C.a(previewurl, C.t('Preview')))

            # original name
            origname = self.document.getname(self.document.info['src'])
            if origname != name:
                print(C.span(
                        '{}: {}'.format(
                        C.t('Original name'),
                        origname),
                    cl='origname'))

            print('</div>')
        
        print('</div>')  # end result box


        
class CLIR:
    def __init__(self,
            language = 'en', url = None,
            host = 'sol2', port = '8971', collection = 'eurosaiall'
            ):
        self.language = language
        if url:
            self.url = url
        else:
            self.url = 'http://{}:{}/solr/{}/select'.format(
            host, port, collection)
        self.host = host
        self.port = port
        self.collection = collection
        self.LIMIT = 200
        self.URLPREFIX = 'http://ufallab.ms.mff.cuni.cz/~rosa/elitr/'

    def t(self, text):
        if text in CLIRtexts.texts and self.language in CLIRtexts.texts[text]:
            return CLIRtexts.texts[text][self.language]
        else:
            return text

    def print_header(self, title='CLIR', nobody=False):
        print('''Content-Type: text/html;charset=utf-8

        <html>
        <head>
            <title>''' + title + '''</title>
            <link rel="stylesheet" type="text/css" href="http://ufallab.ms.mff.cuni.cz/~rosa/elitr/clir.css">
        </head>
        ''')

        if not nobody:
            print('''
            <body>
            <img class="logo"
            src="http://ufallab.ms.mff.cuni.cz/~rosa/elitr/logo_ufal_110u.png"
            alt="Logo ÚFAL" title="Institute of Formal and Applied Linguistics">
            ''')

    def print_footer(self, nohr=False):
        if not nohr:
            print('<hr class="bottomrule">')
        print('''
        <div>
        © 2020 Institute of Formal and Applied Linguistics,
        Faculty of Mathematics and Physics,
        Charles University,
        Prague, Czechia
        </div>
        </body>        
        </html>        
        ''')

    def print_searchform(self):
        print('''<form action="results.py">
                {}: <input name="q" value="foundation"><br>
                <input type="hidden" name="lang" value="{}">
                <input type="hidden" name="host" value="{}">
                <input type="hidden" name="port" value="{}">
                <input type="hidden" name="collection" value="{}">
                <input type="submit" value="{}">
            </form>'''.format(
                self.t('Search query'),
                self.language,
                self.host, self.port, self.collection,
                self.t('Search'),
                ))




    def tag(self, tag, text, cl=None):
        if cl:
            return '<{} class="{}">{}</{}>'.format(tag, cl, text, tag)
        else:
            return '<{}>{}</{}>'.format(tag, text, tag)

    def h1(self, text):
        return self.tag('h1', text)

    def h2(self, text):
        return self.tag('h2', text)

    def a(self, link, text = None):
        if text == None:
            text = link
        return '<a href="' + link + '" target="_blank">' + text + '</a>'

    def p(self, text):
        return self.tag('p', text)

    def div(self, text, cl=None):
        return self.tag('div', text, cl)

    def span(self, text, cl=None):
        return self.tag('span', text, cl)

    def hl(self, text):
        return self.tag('div', text, 'hl')

    def details(self, text):
        return self.tag('div', text, 'details')

    def source(self, text):
        return self.tag('div', text, 'source')

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
