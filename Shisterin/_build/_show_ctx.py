import sys
sys.stdout.reconfigure(encoding='utf-8')
p = r'D:\UP_MobileBank\_build\make_report2_part2.py'
s = open(p, encoding='utf-8').read()
for key in ['40_ставка_ресурса', '41_затраты_после_изменения', '43_отчет_обзор_проекта', '37_связь_нн']:
    i = s.find(key)
    print('=====', key)
    print(s[max(0, i-2200):i+700])
