import sys,re
sys.stdout.reconfigure(encoding='utf-8')
s=open('make_report2.py',encoding='utf-8').read()
for m in re.finditer(r'heading\(doc, "([^"]+)"',s):
 t=m.group(1)
 if re.match(r'1\.',t): print(t)
