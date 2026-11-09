import re, sys
sys.stdout.reconfigure(encoding='utf-8')
p = r'D:\UP_MobileBank\_build\make_report2_part2.py'
s = open(p, encoding='utf-8').read()
s2 = re.sub(r'"Microsoft "\s*\r?\n\s*"Project 2024"', '"программе планирования"', s)
s2 = s2.replace('Microsoft Project 2024','программе планирования').replace('Microsoft Project','программе планирования').replace('MS Project','программе планирования')
if s2 != s:
    open(p,'w',encoding='utf-8').write(s2); print('changed')
else:
    print('same')
i = s2.find('интернет-банка в')
print(repr(s2[i:i+80]))
