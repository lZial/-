import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
s = open("works.py", encoding="utf-8").read()
names = re.findall(r"[\wА-Яа-я0-9_]+\.png", s)
seen = []
for n in names:
    if n not in seen:
        seen.append(n)
for n in seen:
    print(n)
