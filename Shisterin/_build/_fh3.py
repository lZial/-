import sys,re
sys.stdout.reconfigure(encoding='utf-8')
for fn in ('make_report2.py','make_report2_part2.py'):
 s=open(fn,encoding='utf-8').read()
 for m in re.finditer(r'heading\(doc, "([^"]+)"',s):
  t=m.group(1)
  if t=='Введение' or (t and t[0].isdigit()) or 'Приложение' in t or 'Список' in t:
   print(fn.split("2")[-1] if False else fn, '|', t)
