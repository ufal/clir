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
        
        info['datapath'] = datapath
        info['srcdir'] = '/'.join([
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
            metafilename = info['srcdir'] + '/' + info['filename'] + '.meta'
            with open(metafilename) as metafile:
                metadata = json.load(metafile)
                return metadata
        except:
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
            
            previewurl = 'viewdoc.py?lang={}&amp;docid={}'.format(
                    C.language, self.info['datapath'])
            print(C.a(previewurl, C.t('Preview')))

            # language and pages and words
            print('&nbsp;&nbsp;&nbsp;')
            if self.metadata:
                print('{}, {} {}, {} {}'.format(
                    C.t(self.info['src']),
                    self.metadata['pages'],
                    C.t('page' + Result.pluralsuffix(self.metadata['pages'])),
                    self.metadata['words'],
                    C.t('word' + Result.pluralsuffix(self.metadata['words'])),
                    ))
            else:
                print(C.t(self.info['src']))
                
            # translated file
            #trtxt = C.URLPREFIX + self.info['datapath']
            #print(C.a(trtxt, C.t('Translation preview')))
            #print(' ({})'.format(C.t(self.info['lang'])))
            #print('&nbsp;&nbsp;&nbsp;')
            
            # original file
            #srcpdf = C.URLPREFIX + self.info['srcdir'] + '/' + self.info['filename'] + '.pdf'
            #print(C.a(srcpdf, C.t('Original document')))
            #print(' ({})'.format(C.t(self.info['src'])))
            # TODO pages words
            #print('&nbsp;&nbsp;&nbsp;')
            
            # year and SAI
            print('&nbsp;&nbsp;&nbsp;')
            print('{}: {}, {}'.format(
                C.t('Source'),
                C.t('nku_' + self.info['nku']),
                str(self.info['year'])
                ))
            
            # original name
            origname = self.document.getname(self.document.info['src'])
            if origname != name:
                print('&nbsp;&nbsp;&nbsp;')
                print('{}: {}'.format(
                    C.t('Original name'),
                    origname))

            print('</div>')
        print('</div>')

class CLIR:
    def __init__(self, language, url):
        self.language = language
        self.url = url
        self.LIMIT = 200
        self.URLPREFIX = 'http://ufallab.ms.mff.cuni.cz/~rosa/elitr/'

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

    def div(self, text):
        return self.tag('div', text)

    def hl(self, text):
        return self.tag('div', text, 'hl')

    def details(self, text):
        return self.tag('div', text, 'details')

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



    # localization
    texts = {
            'CLIR results': {
                'cs': 'výsledky CLIR',
                },
            'Results for query': {
                'cs': 'Výsledky pro dotaz',
                },
            'Number of results found': {
                'cs': 'Počet nalezených výsledků',
                },
            'CLIR: no query was specified': {
                'cs': 'CLIR: nebyl zadán žádný dotaz',
                },
            'CLIR: no document was specified': {
                'cs': 'CLIR: nebyl zadán žádný dokument',
                },
            'CLIR: cannot display document': {
                'cs': 'CLIR: dokument nelze zobrazit',
                },
            'Translation preview': {
                'cs': 'Náhled překladu',
                },
            'Original document': {
                'cs': 'Původní dokument',
                },
            'nku_be': {
                'cs': 'belgická SAI (Cour des comptes)',
                'de': 'belgische SAI (Cour des comptes)',
                'en': 'Belgian SAI (Cour des comptes)',
                'fr': 'SAI belge (Cour des comptes)',
                },
            'nku_cs': {
                'cs': 'česká SAI (Nejvyšší kontrolní úřad)',
                'de': 'tschechische SAI (Nejvyšší kontrolní úřad)',
                'en': 'Czech SAI (Nejvyšší kontrolní úřad)',
                'fr': 'SAI tchèque (Nejvyšší kontrolní úřad)',
                },
            'nku_de': {
                'cs': 'německá SAI (Bundesrechnungshof)',
                'de': 'deutsche SAI (Bundesrechnungshof)',
                'en': 'German SAI (Bundesrechnungshof)',
                'fr': 'SAI allemand (Bundesrechnungshof)',
                },
            'nku_fr': {
                'cs': 'francouzská SAI (Cour des Comptes)',
                'de': 'französische SAI (Cour des Comptes)',
                'en': 'French SAI (Cour des Comptes)',
                'fr': 'SAI française (Cour des Comptes)',
                },
            'nku_ch': {
                'cs': 'švýcarská SAI (Eidgenössische Finanzkontrolle)',
                'de': 'schweizerische SAI (Eidgenössische Finanzkontrolle)',
                'en': 'Swiss SAI (Eidgenössische Finanzkontrolle)',
                'fr': 'SAI suisse (Eidgenössische Finanzkontrolle)',
                },
            'nku_ir': {
                'cs': 'irská SAI (Office of the Comptroller and Auditor General)',
                'de': 'irlansische SAI (Office of the Comptroller and Auditor General)',
                'en': 'Irish SAI (Office of the Comptroller and Auditor General)',
                'fr': 'SAI irlande (Office of the Comptroller and Auditor General)',
                },
            'nku_ru': {
                'cs': 'ruská SAI (Accounts Chamber of Russian Federation)',
                'de': 'russische SAI (Accounts Chamber of Russian Federation)',
                'en': 'Russian SAI (Accounts Chamber of Russian Federation)',
                'fr': 'SAI russe (Accounts Chamber of Russian Federation)',
                },
            'nku_uk': {
                'cs': 'britská SAI (National Audit Office)',
                'de': 'britische SAI (National Audit Office)',
                'en': 'British SAI (National Audit Office)',
                'fr': 'SAI britannique (National Audit Office)',
                },
            'cs': {
                'cs': 'česky',
                'de': 'tschechisch',
                'en': 'Czech',
                'fr': 'tchèque',
                },
            'de': {
                'cs': 'německy',
                'de': 'deutsch',
                'en': 'German',
                'fr': 'allemand',
                },
            'en': {
                'cs': 'anglicky',
                'de': 'englisch',
                'en': 'English',
                'fr': 'anglais',
                },
            'fr': {
                'cs': 'francouzsky',
                'de': 'französisch',
                'en': 'French',
                'fr': 'français',
                },
            'ru': {
                'cs': 'rusky',
                'de': 'russisch',
                'en': 'Russian',
                'fr': 'SAI russe',
                },
            'Source': {'cs': 'Zdroj',},
            'pages': {'cs': 'stránek',},
            'words': {'cs': 'slov',},
            'page': {'cs': 'stránka',},
            'word': {'cs': 'slovo',},
            'pages2': {'cs': 'stránky', 'en': 'pages'},
            'words2': {'cs': 'slova', 'en': 'words'},
            'Original name': {'cs': 'Původní název',},
            'Preview': {'cs': 'Náhled',},
            '': {'cs': '',},
            '': {'cs': '',},
            '': {'cs': '',},
            '': {'cs': '',},
            '': {'cs': '',},
            
            
            }

