import re, sys
sys.stdout.reconfigure(encoding='utf-8')
p = r'D:\UP_MobileBank\_build\make_report2_part2.py'
s = open(p, encoding='utf-8').read()
# match: в Microsoft "  <newline+indent>  "Project 2024
s2 = re.sub(r'в Microsoft "\s*\r?\n\s*"Project 2024', 'в программе планирования', s)
if s2 == s:
    # try other forms
    s2 = s.replace('Microsoft "\n              "Project 2024', 'программе планирования')
    s2 = s2.replace('Microsoft "\r\n              "Project 2024', 'программе планирования')
open(p,'w',encoding='utf-8').write(s2)
print('changed', s2!=s)
i = s2.find('интернет-банка в')
print(repr(s2[i:i+80]))
print('has MSP', 'Microsoft Project' in s2)
