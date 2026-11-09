def f(p, old, new):
    s=open(p,encoding='utf-8').read(); s=s.replace(old,new); open(p,'w',encoding='utf-8').write(s)
f(r'D:\UP_MobileBank\_build\make_report2.py','""2025-02-03 05:00:00+00:00 -> 03.02.2025.""','"""2025-02-03 05:00:00+00:00 -> 03.02.2025."""')
f(r'D:\UP_MobileBank\_build\make_report2_part2.py','""Сводные строки этапов с числом задач.""','"""Сводные строки этапов с числом задач."""')
f(r'D:\UP_NeuralDefects\_build\make_report2.py','""2025-02-03 05:00:00+00:00 -> 03.02.2025.""','"""2025-02-03 05:00:00+00:00 -> 03.02.2025."""')
print('ok')
