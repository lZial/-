import sys, os
sys.stdout.reconfigure(encoding='utf-8')
for p in [r'D:\UP_MobileBank\_build\make_report2_part2.py', r'D:\UP_NeuralDefects\_build\make_report2_part2.py',
          r'D:\UP_MobileBank\_build\make_report2.py', r'D:\UP_NeuralDefects\_build\make_report2.py']:
    s = open(p, encoding='utf-8').read()
    s2 = s
    s2 = s2.replace('heading(doc, "4.1 Эксперименты с копией плана проекта", 2)', 'heading(doc, "4.17 Анализ чувствительности плана", 2)')
    s2 = s2.replace('heading(doc, "4.17 Эксперименты с копией плана проекта", 2)', 'heading(doc, "4.17 Анализ чувствительности плана", 2)')
    s2 = s2.replace('Microsoft Project 2024', 'программе планирования')
    s2 = s2.replace('Microsoft Project 2025', 'программе планирования')
    s2 = s2.replace('Microsoft Project', 'программе планирования')
    s2 = s2.replace('MS Project 2024', 'программе планирования')
    s2 = s2.replace('MS Project 2025', 'программе планирования')
    s2 = s2.replace('MS Project', 'программе планирования')
    if s2 != s:
        open(p, 'w', encoding='utf-8').write(s2)
        print('fixed', p)
    else:
        print('ok', p)
