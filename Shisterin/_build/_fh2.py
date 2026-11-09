import sys,re
sys.stdout.reconfigure(encoding='utf-8')
for fn in ('make_report2.py','make_report2_part2.py'):
 s=open(fn,encoding='utf-8').read()
 for m in re.finditer(r'heading\(doc, "([^"]+)"', s):
  line=s[:m.start()].count('\n')+1
  t=m.group(1)
  if t=='Введение' or re.match(r'\d',t) or 'Приложение' in t or 'Список' in t:
   print(fn,line,t)
