import sys
sys.stdout.reconfigure(encoding='utf-8')
for p in ('make_report2.py','make_report2_part2.py'):
    s=open(p,encoding='utf-8').read()
    s=s.replace('праздничных дней 2026 года','праздничных дней 2025 года')
    s=s.replace('соответственно на 4 мая и 15 июня 2026 года.','с учётом переносов выходных дней в 2025 году.')
    s=s.replace('апреле 2026','апреле 2025').replace('2026 года','2025 года')
    if '2026' in s:
        for i,l in enumerate(s.splitlines(),1):
            if '2026' in l: print(p,i,l.strip()[:140])
    open(p,'w',encoding='utf-8').write(s)
    print(p, '2026 left', s.count('2026'))
