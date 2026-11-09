import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')
for root in [r'D:\UP_MobileBank\_build', r'D:\UP_NeuralDefects\_build']:
    print('===', root)
    for fn in ('make_report.py', 'make_report2.py', 'make_report2_part2.py', 'works.py'):
        p = os.path.join(root, fn)
        if not os.path.exists(p):
            continue
        lines = open(p, encoding='utf-8').read().splitlines()
        for i, l in enumerate(lines):
            if re.search(r'[0-9]{2}_[^"\']+\.png', l):
                print(fn, i+1, l.strip()[:150])
