import sys, re
sys.stdout.reconfigure(encoding='utf-8')
p='make_report2_part2.py'
s=open(p,encoding='utf-8').read()
s=re.sub(r'para\(doc,\s*"Все шестнадцать практических работ выполнены.*?" % BASENAME\)',
         'para(doc, "Для проекта подготовлен план в файле «%s.mpp». Ниже показаны основные шаги настройки плана и учёта выполнения с пояснениями и снимками экрана." % BASENAME)',
         s, count=1, flags=re.S)
s=s.replace('(таблица 4.3);', 'приведены в таблице ниже;')
s=s.replace('(Таблица 4.3);', 'приведены в таблице ниже;')
s=re.sub(r'Все шестнадцать практических работ выполнены в одном файле проекта[^.]*\.',
         'План проекта, ресурсы, календарь, зависимости, базовый план, фактические данные и диаграмма Ганта собраны в одном файле и согласованы между собой.', s)
body, sep, tail = s.partition('SOURCES = [')
body=re.sub(r'практическ\w*\s+работ\w*','работ', body, flags=re.I)
s = body + sep + tail
open(p,'w',encoding='utf-8').write(s)
b2 = s.partition('SOURCES = [')[0]
for pat in ['практическ','таблица 4.3']:
    ms=re.findall(pat,b2,re.I)
    if ms: print('LEFT',pat,ms)
print('ok')
