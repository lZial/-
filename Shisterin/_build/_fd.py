s=open('make_report2_part2.py',encoding='utf-8').read()
if s.startswith('""Разделы') or s.startswith('""\u0420'): s='"""'+s[2:]
open('make_report2_part2.py','w',encoding='utf-8').write(s); print(repr(s[:30]))
