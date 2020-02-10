#!/usr/bin/env python3
#coding: utf-8

import requests
import json
import re
from clir_texts import CLIRtexts
import sys

import locale

lstripchars = '!"“#$%&\'’)*+,-–./:;=?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
rstripchars = '!"„#$%&\'’(*+,-–./:;=?@[\\]^_`{|}~ \t\n\r\x0b\x0c'

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


    def show_parallel(self, C, query = None):
        trfilename  = '.' + self.info['datapath']
        srcfilename = '.' + self.get_source_txt()
        if query:
            query = query.split()
        else:
            query = []
        try:
            with open(trfilename, encoding='utf8') as trfile, open(srcfilename, encoding='utf8') as srcfile:
                print('<table class="paratable">')
                print('''<thead>
                    <tr>
                    <th class="left">{}</th>
                    <th class="right">{}</th>
                    </tr>
                    </thead>'''.format(
                    C.t('Automatic translation'), C.t('Original text')))
                print('<tbody>')
                for trline, srcline in zip(trfile, srcfile):
                    if trline != '\n' and srcline != '\n':
                        print('<tr><td>{}</td><td>{}</td></tr>'.format(
                            C.highlight(trline, query),
                            srcline))
                print('</tbody>')
                print('</table>')
        except:
            logging.error(sys.exc_info()[0])
            print(C.p(C.t('Error ocurred while opening the document.')))

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

    # year and SAI
    def info_sai_year(self, C):
        result = ''
        if self.info:
            result = '{}, {}'.format(
                C.t('nku_' + self.info['nku']),
                str(self.info['year'])
                )
        return result

    # language and pages and words
    def info_lang_p_w(self, C):
        result = ''
        if self.info:
            result = C.t(self.info['src'])
            if self.metadata and 'pages' in self.metadata:
                result = '{}, {} {}'.format(
                    result,
                    self.metadata['pages'],
                    C.t('page' + Result.pluralsuffix(self.metadata['pages'])),
                )
            if self.metadata and 'words' in self.metadata:
                result = '{}, {:n} {}'.format(
                    result,
                    self.metadata['words'],
                    C.t('word' + Result.pluralsuffix(self.metadata['words'])),
                )
        return result

    # file ID -- not the full one, just the filename without extension
    def info_id(self, C):
        result = ''
        if self.info:
            name = self.document.getname(C.language)
            if self.info['filename'] != name:
                result = '{}: {}'.format(
                            C.t('ID'),
                            self.info['filename'])
        return result

    # Original name
    def info_origname(self, C):
        result = ''
        if self.info:
            name = self.document.getname(C.language)
            origname = self.document.getname(self.document.info['src'])
            if origname != name:
                result = '{}: {}'.format(
                    C.t('Original name'),
                    origname)
        return result

    # Preview link
    def info_previewurl(self, C):
        if self.info:
            return 'viewdoc.py?lang={}&amp;docid={}&amp;q={}'.format(
                    C.language, self.info['datapath'], C.searchquery)
        else:
            return None

    def show(self, C):
        # Get data
        name = self.document.getname(C.language)
        info_sai_year   = self.info_sai_year(C)
        info_lang_p_w   = self.info_lang_p_w(C)
        info_id         = self.info_id(C)
        info_origname   = self.info_origname(C)
        info_previewurl = self.info_previewurl(C)
        
        # Start output
        print('<div class="result" id="' + self.docid + '">')
        
        # Details box
        print(C.div(
            C.div(info_id, cl='id') +
            C.div(info_sai_year, cl='source') + 
            C.div(info_lang_p_w, cl='lang'),
            cl='details'))

        # Document name
        if info_previewurl:
            print(C.h2(C.a(info_previewurl, name)))
        else:
            print(C.h2(name))
            
        # Search results highlight
        print(self.hldiv(C))

        # Original name
        print(C.div(C.span(info_origname, 'origname')))

        # Clearer
        print(C.div('', cl='clearer'))

        # End output
        print('</div>')

    # search results highlight
    def hldiv(self, C):
        hltext = ''
        if self.hl:
            hltext = self.hl
            hlclasses = 'bqh hl ahq' # before quote hellip, highlight, after hellip quote
            hltext = hltext.lstrip(lstripchars)
            hltext = hltext.rstrip(rstripchars)
        else:
            if len(self.content) < C.LIMIT:
                hltext = self.content
                hlclasses = 'bq hl aq' # before quote, highlight, after quote
                hltext = hltext.strip()
            else:
                hltext = self.content[:C.LIMIT]
                last_space = hltext.rfind(' ')
                hltext = hltext[:last_space] # break at word boundary
                hltext = hltext.lstrip()
                hltext = hltext.rstrip(rstripchars)
                hlclasses = 'bq hl ahq' # before quote, highlight, after hellip quote
        
        return C.tag('div', hltext, hlclasses)
        
lang2locale = {
    'cs': 'cs_CZ.UTF-8',
#    'de': 'de_DE.UTF-8',
    'en': 'en_US.UTF-8',
#    'fr': 'fr_FR.UTF-8',
}

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
        self.LIMIT = 150
        self.URLPREFIX = 'http://ufallab.ms.mff.cuni.cz/~rosa/elitr/'

        if language in lang2locale:
            locale.setlocale(locale.LC_ALL, lang2locale[language])
        else:
            locale.setlocale(locale.LC_ALL, lang2locale['en'])


    def get_results(self, q):
        lang_filter = 'id:*/data_{}/*'.format(self.language)
        data = {'q': q,
                'hl': 'true', # highlighting
                'hl.fl' : 'content', # what to highlight
                'rows': 100,
                'fq': lang_filter,
                }
        # highlighting->id->content[0] ... <em> highlights search query
        response = requests.get(self.url, data = data)
        #response.encoding='utf8'
        return Results(response)

    def show_results(self, results):
        for result in results.results:
            result.show(self)

    def t(self, text):
        if text in CLIRtexts.texts and self.language in CLIRtexts.texts[text]:
            return CLIRtexts.texts[text][self.language]
        else:
            return text

    def highlight(self, text, words):
        search = '(' + '|'.join([re.escape(word) for word in words]) + ')'
        replace = self.tag('span', r'\1', 'highlight')
        regex = re.compile(search, re.IGNORECASE)
        text = regex.sub(replace, text)
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
                {}: <input name="q" value="Praha"><br>
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

    def a(self, link, text = None, targetblank = False):
        if text == None:
            text = link
        tb = ' target="_blank"' if targetblank else ''
        return '<a href="{}"{}>{}</a>'.format(link, tb, text)

    def p(self, text, cl=None):
        return self.tag('p', text, cl)

    def div(self, text, cl=None):
        return self.tag('div', text, cl)

    def span(self, text, cl=None):
        return self.tag('span', text, cl)
