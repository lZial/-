s=open('make_report.py',encoding='utf-8').read()
s=s.replace('YEAR = "2026"','YEAR = "2025"').replace("YEAR = '2026'","YEAR = '2025'")
s=s.replace('2026','2025')
open('make_report.py','w',encoding='utf-8').write(s); print(s.count('2026'))
