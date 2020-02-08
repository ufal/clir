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
    return response

# how many characters max to send to translation
# Lindat Translate has limit of 100 kB for input
LIMIT=50000
LIMIT=1000

logging.info('Welcome to transformer!')

if len(sys.argv) < 4:
    sys.exit('Usage: ./' + sys.argv[0] + ' infile srclang tgtlang > outfile')

# TODO it would be nice to also support stdin, but I don't need that now

infilename, srclang, tgtlang = sys.argv[1:4]
logging.info('Translate ' + infilename + ' from ' + srclang + ' to ' + tgtlang)
infile = open(infilename, 'r')

# URL of the endpoint
url = 'http://lindat.mff.cuni.cz/services/translation/api/v2/models/' + srclang + '-' + tgtlang
headers = {"accept": "text/plain"}

# translate each reasonably sized chunk (and then the last remaining chunk)
data = {}
text = []
textlen = 0
result = []
ok = True

def trtext():
    global data, text, textlen, result, ok
    data["input_text"] = ''.join(text)
    #logging.info(str(text))
    logging.info('Translating a batch of ' + str(len(text)) + ' lines')
    response = translate(url, data, headers)
    if response.ok:
        result.append(response.text)
        text = []
        textlen = 0
        return True
    else:
        ok = False
        return False

# translate large chunks
for line in infile:
    text.append(line)
    textlen += len(line)
    if textlen > LIMIT:
        if not trtext():
            break
# translate what remains
if textlen > 0:
    trtext()

# TODO last chunk tends to contain an extra \n at the end, I don't know why
if ok:
    logging.info('Writing out the results.')
    #logging.info(str(result))
    print(*result, sep='', end='')  # \n already ends each chunk; this ensures lines will match
    logging.info('All good, bye!')
else:
    logging.info('Not writing out any results because there was an error.')
    logging.info('Sorry, bye!')

infile.close()
