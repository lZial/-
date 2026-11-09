import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')
for root in [r'D:\UP_MobileBank\_build', r'D:\UP_NeuralDefects\_build']:
    print('===', root)
    for fn in ('make_report.py', 'make_report2.py', 'make_report2_part2.py', 'works.py'):
        p = os.path.join(root, fn)
        if not os.path.exists(p):
            continue
        s = open(p, encoding='utf-8').read()
        for m in re.finditer(r'\(\s*"([0-9]{2}_[^"]+\.png)"\s*,\s*"([^"]*)"\s*\)', s, re.S):
            print(m.group(1), '|', ' '.join(m.group(2).split())[:120])
