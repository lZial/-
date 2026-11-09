import sys
sys.stdout.reconfigure(encoding='utf-8')
p=r'D:\UP_MobileBank\_build\make_report2.py'
s=open(p,encoding='utf-8').read()
# boundaries: each heading start to next
b11=s.find('heading(doc, "1.1 Понятие')
b12=s.find('heading(doc, "1.2 Целевая')
b13=s.find('heading(doc, "1.3 Архитектура')
b14=s.find('heading(doc, "1.4 Анализ рынка')
b15=s.find('heading(doc, "1.5 Нормативное')
b16=s.find('heading(doc, "1.6 Необходимость')
b2 =s.find('heading(doc, "2 Анализ модели')
assert all(x>=0 for x in [b11,b12,b13,b14,b15,b16,b2])
blk11=s[b11:b12]; blk12=s[b12:b13]; blk13=s[b13:b14]; blk14=s[b14:b15]; blk15=s[b15:b16]; blk16=s[b16:b2]
# logical: 1.1,1.2,1.4,1.6,1.3,1.5
s=s[:b11]+blk11+blk12+blk14+blk16+blk13+blk15+s[b2:]
open(p,'w',encoding='utf-8').write(s)
print('ok')
