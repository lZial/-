import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
root = r'D:\UP_MobileBank\_build'
for fn in sorted(os.listdir(root)):
    if not fn.endswith('.py'):
        continue
    s = open(os.path.join(root, fn), encoding='utf-8').read()
    names = re.findall(r'([0-9]{2}_[^"\']+?\.png)', s)
    if names:
        print(fn, '->', sorted(set(names)))
