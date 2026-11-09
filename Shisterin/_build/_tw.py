import re,sys
sys.stdout.reconfigure(encoding='utf-8')
s=open('make_report.py',encoding='utf-8').read()
titles=re.findall(r'"title":\s*"([^"]+)"',s)
print(len(titles))
for t in titles: print(t)
