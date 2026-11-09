import sys,re
sys.stdout.reconfigure(encoding='utf-8')
for fn in ('make_report2.py','make_report2_part2.py'):
 s=open(fn,encoding='utf-8').read()
 for m in re.finditer(r'heading\(doc, "(\d+(?:\.\d+)?) ([^"]+)"', s):
  line=s[:m.start()].count('\n')+1
  print(fn,line,m.group(1),m.group(2)[:70])
