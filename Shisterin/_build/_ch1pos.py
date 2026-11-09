import sys
sys.stdout.reconfigure(encoding='utf-8')
s=open('make_report2.py',encoding='utf-8').read()
markers=['1.1 Понятие','1.2 Целевая','1.3 Архитектура','1.4 Анализ рынка','1.5 Нормативное','1.6 Необходимость','2 Анализ модели']
pos=[]
for m in markers:
 i=s.find(m)
 if i>=0: pos.append((m, s.rfind('heading(doc',0,i)))
for m,h in pos: print(m,h)
