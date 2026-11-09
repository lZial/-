import sys
from docx import Document
sys.stdout.reconfigure(encoding='utf-8')
for name, path in [('SH', r'D:\UP_MobileBank\УП_Шистерин.docx'), ('MA', r'D:\UP_NeuralDefects\УП_Матвих.docx')]:
    d = Document(path)
    paras = d.paragraphs
    print('==', name)
    # check blank after headings
    missing = []
    for i, p in enumerate(paras):
        st = p.style.name if p.style else ''
        if 'Heading' in st and p.text.strip():
            # next paragraph should be empty/blank
            if i+1 < len(paras):
                nxt = paras[i+1]
                if nxt.text.strip() != '' or (nxt.style and 'Heading' in nxt.style.name):
                    # allow if next is a table? paragraphs don't show tables; sometimes figure is in para
                    missing.append((i, st, p.text.strip()[:60], nxt.text.strip()[:40], nxt.style.name if nxt.style else ''))
    print(' headings missing blank after:', len(missing))
    for m in missing[:12]:
        print(' ', m)
    # long blank runs
    blank_run = 0
    max_blank = 0
    for p in paras:
        if not p.text.strip() and not p._element.xpath('.//w:drawing') and not p._element.xpath('.//w:pict'):
            blank_run += 1
            max_blank = max(max_blank, blank_run)
        else:
            blank_run = 0
    print(' max consecutive blank paras:', max_blank)
    # figures/tables quick
    import re
    full = '\n'.join(p.text for p in paras)
    figs = re.findall(r'^Рисунок \d+', full, re.M)
    tabs = re.findall(r'^Таблица \d+', full, re.M)
    print(' figs', len(figs), 'tabs', len(tabs), '2026', len(re.findall('2026', full)))
