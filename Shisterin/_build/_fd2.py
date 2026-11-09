s=open('make_report2_part2.py',encoding='utf-8').read()
# fix first docstring ending: ensure triple quotes
lines=s.splitlines(True)
if lines and lines[0].rstrip().endswith('.""') and not lines[0].rstrip().endswith('."""'):
    lines[0]=lines[0].replace(').""', ')."""')
s=''.join(lines)
open('make_report2_part2.py','w',encoding='utf-8').write(s); print(lines[0].rstrip()[-10:])
