import re, sys
sys.stdout.reconfigure(encoding='utf-8')
s = open('make_report2_part2.py', encoding='utf-8').read()
for m in re.finditer(r'heading\(doc,\s*"([^"]+)"', s):
    print(m.group(1))
