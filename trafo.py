#!/usr/bin/env python3
#coding: utf-8

import requests
import sys

import logging
logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

def translate(url, data, headers):
    logging.info('Sending request: ' + str(len(data["input_text"])) + ' characters')
    response = requests.post(url, data = data, headers = headers)
    logging.info('Got response ' + str(response.status_code) + ' ' + response.reason)
    response.encoding='utf8'

# how many characters max to send to translation
# Lindat Translate has limit of 100 kB for input
LIMIT=50000

logging.info('Welcome to transformer!')

if len(sys.argv) < 4:
    sys.exit('Usage: ./' + sys.argv[0] + ' infile srclang tgtlang > outfile')

# TODO it would be nice to also support stdin, but I don't need that now

infilename, srclang, tgtlang = sys.argv[1:4]
logging.info('Translate ' + infilename + ' from ' + srclang + ' to ' + tgtlang)
infile = open(sys.argv[1], 'r')
text = infile.read()
infile.close()
logging.info('File size is ' + str(len(text)) + ' characters')

# URL of the endpoint
url = 'http://lindat.mff.cuni.cz/services/translation/api/v2/models/' + srclang + '-' + tgtlang
headers = {"accept": "text/plain"}

result = []
ok = True

    data = {"input_text": text}
    response = translate(url, data, headers)
    if response.ok:
        logging.info('All good, bye!')
        return response.text
    else:
        logging.info('ERROR')
        return ''

if ok:
    logging.info('Writing out the results.')
    print(*result, sep='\n')
    logging.info('All good, bye!')
else:
    logging.info('Not writing out any results because there was an error.')
    logging.info('Sorry, bye!')

