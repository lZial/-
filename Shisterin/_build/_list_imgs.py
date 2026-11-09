import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')
for root in [r'D:\UP_MobileBank', r'D:\UP_NeuralDefects']:
    build = os.path.join(root, '_build')
    shots = os.path.join(root, 'Скриншоты')
    print('===', root)
    all_imgs = []
    for fn in ('make_report.py', 'make_report2.py', 'make_report2_part2.py', 'works.py'):
        p = os.path.join(build, fn)
        if not os.path.exists(p):
            continue
        s = open(p, encoding='utf-8').read()
        imgs = re.findall(r'([0-9]{2}_[^"\']+\.png)', s)
        for i in imgs:
            if i not in all_imgs:
                all_imgs.append(i)
    print('referenced', len(all_imgs))
    have = set(os.listdir(shots))
    missing = [i for i in all_imgs if i not in have]
    unused = [i for i in sorted(have) if i not in all_imgs]
    print('missing:', missing)
    print('unused:', unused)
