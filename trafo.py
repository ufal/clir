#!/usr/bin/env python3
#coding: utf-8

import requests
import sys

import logging
logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

logging.info('Welcome to transformer!')

if len(sys.argv) > 1:
    logging.info('Input from ' + sys.argv[1])
    infile = open(sys.argv[1], 'r')
    text = infile.read()
else:
    logging.info('Input from STDIN')
    text = sys.stdin.read()

# you need to find out what the URL of the endpoint is
url = 'http://lindat.mff.cuni.cz/services/translation/api/v2/models/en-cs'

# you need to find out what parameters the API expects
#data = {"input_text": "I want to go for a beer today."}
data = {"input_text": text}

# sometimes, you may need to specify some headers (often not necessary)
headers = {"accept": "text/plain"}

# some APIs support `get`, some support `post`, some support both
logging.info('Sending request: ' + str(len(text)) + ' characters')
#logging.info('Sending request ' + str(data))
response = requests.post(url, data = data, headers = headers)
logging.info('Got response ' + str(response.status_code) + ' ' + response.reason)
response.encoding='utf8'

if response.ok:
    print(response.text)
    logging.info('All good, bye!')
else:
    logging.info('ERROR')
