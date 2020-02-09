#!venv/bin/python 

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Content-Type: text/html;charset=utf-8")
print("")
print("TODO Tady bude CLIR demo na Elitr Eurosai 2020 Workshop", end='<br>')
print('<a href="input.py">Multilingvální testovací verze</a>', end='<br>')
print('<a href="input.py?lang=cs">Multilingvální testovací verze CS</a>', end='<br>')
print('<a href="input.py?lang=en">Multilingvální testovací verze EN</a>', end='<br>')
print('<a href="input.py?lang=de">Multilingvální testovací verze DE</a>', end='<br>')
print('<a href="input.py?lang=fr">Multilingvální testovací verze FR</a>', end='<br>')
print('<a href="vstup.php">Starší testovací verze</a>', end='<br>')

