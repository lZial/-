import sys, os
sys.stdout.reconfigure(encoding='utf-8')

# SH: find conclusion text with Microsoft Project
for fn in ('make_report2_part2.py','make_report2.py','make_report.py'):
    p = os.path.join(r'D:\UP_MobileBank\_build', fn)
    s = open(p, encoding='utf-8').read()
    s2 = s.replace('Microsoft Project 2024', 'программе планирования').replace('Microsoft Project 2025', 'программе планирования').replace('Microsoft Project', 'программе планирования').replace('MS Project 2024','программе планирования').replace('MS Project','программе планирования')
    if s2 != s:
        open(p,'w',encoding='utf-8').write(s2)
        print('fixed', fn)

# body text consistency
for p in [r'D:\UP_MobileBank\_build\make_report2_part2.py', r'D:\UP_NeuralDefects\_build\make_report2_part2.py']:
    s = open(p, encoding='utf-8').read()
    s2 = s.replace('Эксперименты с копией плана "', 'Анализ чувствительности плана (копия файла) "')
    # collapse the broken string concat in replacement context - easier: targeted
    s2 = s2.replace('Анализ чувствительности плана (копия файла) "\n              "показали', 'Анализ чувствительности плана показал')
    if s2 != s:
        open(p,'w',encoding='utf-8').write(s2)
        print('fixed exp text', p)
    else:
        print('no exp', p)
