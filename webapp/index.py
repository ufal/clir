#!/usr/bin/env python3

import sys
import io
import json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Content-Type: text/html;charset=utf-8")
print("")

with open('clir.cfg') as configfile:
    cfg = json.load(configfile)

print('''<html>
<head>
    <title>CLIR demo</title>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="{0}/static/clir.css">
</head>
<body>
<img class="logo"
src="{0}/static/logo_ufal_110u.png"
alt="Logo ÚFAL" title="Institute of Formal and Applied Linguistics">
'''.format(cfg['staticurl']))

print('''<h1>CLIR demo</h1>
<p>Eurosai 2020 LangTools Workshop</p>
<hr>
<h2><a href="{0}/input.py?lang=en">English</a> (EN)</h2>
<h2><a href="{0}/input.py?lang=de">Deutsch</a> (DE)</h2>
<h2><a href="{0}/input.py?lang=fr">Français</a> (FR)</h2>
<h2><a href="{0}/input.py?lang=cs">Česky</a> (CS)</h2>
'''.format(cfg['dynurl']))

print('''
<hr>
<div>
© 2020 Institute of Formal and Applied Linguistics,
Faculty of Mathematics and Physics,
Charles University,
Prague, Czechia
</div>
</body>        
</html>        
''')

