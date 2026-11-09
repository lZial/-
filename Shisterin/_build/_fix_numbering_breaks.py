import sys, re, glob, os
sys.stdout.reconfigure(encoding='utf-8')

def fix_file(path):
    s = open(path, encoding='utf-8').read()
    orig = s
    # 1) "1 Введение" -> "Введение" (no number)
    s = s.replace('heading(doc, "1 Введение", 1)', 'heading(doc, "Введение", 1)')
    s = s.replace("heading(doc, '1 Введение', 1)", "heading(doc, 'Введение', 1)")
    # 2) shift "N ..." and "N.M ..." down by 1 for N>=2
    def repl(m):
        pre, num, rest = m.group(1), m.group(2), m.group(3)
        if '.' in num:
            a,b = num.split('.',1)
            a = int(a)
            if a <= 1: return m.group(0)
            return '%s"%d.%s%s' % (pre, a-1, b, rest)
        else:
            n = int(num)
            if n <= 1: return m.group(0)
            return '%s"%d %s' % (pre, n-1, rest)
    s = re.sub(r'(heading\(doc, ")(\d+(?:\.\d+)?)( [^"]+")', repl, s)
    # 3) remove excessive page breaks (keep after title/contents area heuristic: lines calling page_break not before Приложение headings in part2? easier targeted)
    if 'make_report2_part2' in path.replace('\\','/'):
        # remove page_breaks before major sections 4-8 and between A/B/C apps (keep around section/orientation changes as needed)
        for old in [
            '\n    page_break(doc)\n    heading(doc, "4 ',
            '\n    page_break(doc)\n    heading(doc, "5 ',
            '\n    page_break(doc)\n    heading(doc, "6 ',
            '\n    page_break(doc)\n    heading(doc, "7 ',
            '\n    page_break(doc)\n    heading(doc, "8 ',
            '\n    page_break(doc)\n    heading(doc, "Приложение Б"',
            '\n    page_break(doc)\n    heading(doc, "Приложение В"',
            '\n    page_break(doc)\n    heading(doc, "Приложение Г"',
        ]:
            s = s.replace(old, '\n    ' + old.split('heading',1)[1].join(['heading',''])) if False else s
    # simpler: targeted removals by patterns
    # in make_report2.py remove breaks before section 2/3 and 5-experiments area? 219 before "2 Обзор" became "1 Обзор"? better remove specific page_break lines by context
    if 'make_report2_part2' in path.replace('\\','/'):
        s = re.sub(r'\n    page_break\(doc\)\n(    heading\(doc, "[4-8] )', r'\n\1', s)
        s = re.sub(r'\n    page_break\(doc\)\n(    heading\(doc, "Приложение [БВГ]")', r'\n\1', s)
    if path.endswith('make_report2.py') and 'NeuralDefects' not in path and 'MobileBank' not in path:
        pass
    # generic for make_report2.py: remove page_break before "1 Обзор предметной" (was 2) and before "2 Анализ" (was 3) and before "5 Реализация"? check
    base = os.path.basename(path)
    if base == 'make_report2.py':
        s = re.sub(r'\n    page_break\(doc\)\n(    heading\(doc, "[12] Обзор предметной)', r'\n\1', s)
        s = re.sub(r'\n    page_break\(doc\)\n(    heading\(doc, "[23] Анализ модели)', r'\n\1', s)
    # remove keep_with_next on normal headings? heading() sets keep=True; can cause gaps. change in make_report.py is better, but per request just avoid big gaps - try keep=False in heading by patching call style? heading() is in make_report.py; patch there once.
    if s != orig:
        open(path,'w',encoding='utf-8').write(s)
        print('fixed', path)
    else:
        print('no change', path)

for root in [r'D:\UP_MobileBank\_build', r'D:\UP_NeuralDefects\_build']:
    for fn in ('make_report2.py','make_report2_part2.py'):
        p = os.path.join(root,fn)
        if os.path.exists(p): fix_file(p)
