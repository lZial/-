import os, sys
sys.stdout.reconfigure(encoding='utf-8')

def fix_make_report2(path):
    lines=open(path,encoding='utf-8').readlines()
    # fix broken docstring at top
    if lines[0].strip() in ('""', '"', "''"):
        # find where imports start
        j=1
        while j<len(lines) and not lines[j].startswith(('import ','from ','sys.','BUILD ','SHOTS','BASE ','CFG ','import\r','from\r')):
            j+=1
        # wrap 0..j-1 as docstring
        body=''.join(lines[1:j]).rstrip()+'\n'
        lines=['"""%s"""\n' % body.lstrip()] + ['\n'] + lines[j:]
    open(path,'w',encoding='utf-8').writelines(lines)
    print('ok', path)

def fix_part2(path):
    s=open(path,encoding='utf-8').read()
    s=s.replace('""Сводные задачи этапов с числом входящих рабочих задач.""',
                '"""Сводные задачи этапов с числом входящих рабочих задач."""')
    # fix broken empty strings in row
    s=s.replace('rows.append([", "Итого по проекту", ", ", "03.02.2025", "18.08.2025", ", "6 597 000 руб."])',
                'rows.append(["", "Итого по проекту", "", "", "03.02.2025", "18.08.2025", "", "6 597 000 руб."])')
    s=s.replace('rows.append([", "Итого по проекту", ", ", "03.02.2025", "18.08.2025", ", money(BUDGET)])',
                'rows.append(["", "Итого по проекту", "", "", "03.02.2025", "18.08.2025", "", money(BUDGET)])')
    s=s.replace('rows.append([" , "Итого по проекту"','rows.append(["", "Итого по проекту"')
    open(path,'w',encoding='utf-8').write(s)
    print('ok', path)

for root in [r'D:\UP_MobileBank\_build', r'D:\UP_NeuralDefects\_build']:
    fix_make_report2(os.path.join(root,'make_report2.py'))
    fix_part2(os.path.join(root,'make_report2_part2.py'))
