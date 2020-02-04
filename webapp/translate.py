#!venv/bin/python 
#coding: utf-8

import requests

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Content-Type: text/plain;charset=utf-8")
print("")

# you need to find out what the URL of the endpoint is
url = 'http://lindat.mff.cuni.cz/services/translation/api/v2/models/en-cs'

# you need to find out what parameters the API expects
data = {"input_text": "I want to go for a beer today."}

# sometimes, you may need to specify some headers (often not necessary)
headers = {"accept": "text/plain"}

# some APIs support `get`, some support `post`, some support both
response = requests.post(url, data = data, headers = headers)
response.encoding='utf8'
print(response.text)


