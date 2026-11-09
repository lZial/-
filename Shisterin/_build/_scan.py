import re,sys,os
sys.stdout.reconfigure(encoding='utf-8')
for root in [r'D:\UP_MobileBank\_build',r'D:\UP_NeuralDefects\_build']:
    for fn in ('make_report.py','make_report2.py','make_report2_part2.py','works.py'):
        p=os.path.join(root,fn)
        if not os.path.exists(p): continue
        s=open(p,encoding='utf-8').read()
        body=s.split('SOURCES = [')[0]
        m=re.findall('.{0,20}2026.{0,20}',body)
        if m: print(p, '2026', len(m), m[0])
        m=re.findall(r'MS Project 2024|Microsoft Project 2024',s)
        if m: print(p,'MSP2024',len(m))
