#!venv/bin/python 

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Content-Type: text/html;charset=utf-8")
print("")
print("TODO Tady bude CLIR demo na Elitr Eurosai 2020 Workshop", end='<br>')
print('<a href="vstup.php">Testovací verze</a>', end='<br>')
print('<a href="vstup2.php">Testovací verze 2</a>', end='<br>')

