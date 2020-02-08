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
    
    logging.info('Translating a batch of ' + str(len(text)) + ' lines')
    
    # !!! Transformer tends to eat up empty lines at the beginning
    # so we need to keep them away and readd them later
    # To be sure, let's do the same with empty lines at the end.
    # Also it tends to add a newline to the end of the output, so we strip
    # that (Since we remove final empties, we can simply rstrip the result.)
    # I hope that empty lines inside the text are fine
    # (it seems so from what I have seen)
    initial_empties = 0
    while text[initial_empties] == '':
        initial_empties += 1
    final_empties = 0
    while text[-final_empties-1] == '':
        final_empties += 1
    stripped_text = text[initial_empties:len(text)-final_empties]
    
    data["input_text"] = '\n'.join(stripped_text)
    response = translate(url, data, headers)
    if response.ok:       
        # put back the initial empty lines
        for _ in range(initial_empties):
            result.append('')
        # put there the translation
        result.append(response.text.rstrip())
        # put back the final empty lines
        for _ in range(final_empties):
            result.append('')
        text = []
        textlen = 0
        return True
    else:
        ok = False
        return False

# translate large chunks
for line in infile:
    # we will handle newlines extra since Transformer mixes up empty lines
    stripline = line.rstrip()
    text.append(stripline)
    textlen += len(stripline)
    if textlen > LIMIT:
        if not trtext():
            break
# translate what remains
if ok and len(text) > 0:
    if textlen > 0:
        # there are some non-empty lines
        trtext()
    else:
        # there are just empty lines
        result.extend(text)

# NOTE: if the input file does not end with a newline, the outputfile
# will be one line longer, because we always want the output file to end
# with a newline
if ok:
    logging.info('Writing out the results.')
    print(*result, sep='\n', end='\n')
    logging.info('All good, bye!')
else:
    logging.info('Not writing out any results because there was an error.')
    logging.info('Sorry, bye!')

infile.close()
