import sys
sys.stdout.reconfigure(encoding='utf-8')
for p in [r'D:\UP_MobileBank\_build\make_report2_part2.py', r'D:\UP_NeuralDefects\_build\make_report2_part2.py']:
    s = open(p, encoding='utf-8').read()
    s = s.replace('"Microsoft "\n              "Project 2024"', '"программе планирования"')
    s = s.replace('в Microsoft Project 2024', 'в программе планирования')
    s = s.replace('в Microsoft Project', 'в программе планирования')
    if 'Microsoft Project' in s or 'MS Project' in s:
        print('STILL', p)
    open(p,'w',encoding='utf-8').write(s)
    print('ok', p)
