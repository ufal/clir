#!venv/bin/python 

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Content-Type: text/plain;charset=utf-8")
print("")

import requests
import json

animal = 'cat'
url = 'https://cat-fact.herokuapp.com/facts/random?animal_type=' + animal
response = requests.get(url)
j = json.loads(response.text)
print(j['text'])
print()

url = 'http://lindat.mff.cuni.cz/services/translation/api/v2/models/en-cs'
data = {"input_text": j['text']}
headers = {"accept": "text/plain"}
response = requests.post(url, data = data, headers = headers)
response.encoding='utf8'
print(response.text)


