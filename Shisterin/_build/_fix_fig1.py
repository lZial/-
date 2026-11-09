s=open('make_report.py',encoding='utf-8').read()
old = r'''def figure(doc, filename, caption, width_cm=16.0, number=True):
    path = os.path.join(SHOTS, filename)
    if not os.path.exists(path):
        para(doc, "[изображение отсутствует: %s]" % filename, italic=True)
        return
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.add_run().add_picture(path, width=Cm(width_cm))
    cap = caption
    if number and "Рисунок" in cap:
        # сквозная нумерация: берём текст после тире
        txt = cap
        for sep in (" – ", " - ", "—"):
            if sep in txt:
                txt = txt.split(sep, 1)[1]
                break
        else:
            parts = txt.split(None, 2)
            txt = parts[2] if len(parts) > 2 else txt
        cap = "Рисунок %d – %s" % (next_fig(), txt.strip())
    elif number:
        cap = "Рисунок %d – %s" % (next_fig(), cap.strip())
    cp = para(doc, cap, size=12, align="center", indent=0, spacing=1.0, before=0, after=0)
    for r in cp.runs:
        r.italic = False'''
new = r'''def figure(doc, filename, caption, width_cm=16.0, number=True):
    path = os.path.join(SHOTS, filename)
    if not os.path.exists(path):
        para(doc, "[изображение отсутствует: %s]" % filename, italic=True)
        return
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.add_run().add_picture(path, width=Cm(width_cm))
    if number:
        cap = "Рисунок %d" % next_fig()
    else:
        cap = caption
    cp = para(doc, cap, size=12, align="center", indent=0, spacing=1.0, before=0, after=0)
    for r in cp.runs:
        r.italic = False'''
# try LF
old_lf = old.replace('\r\n','\n')
s_lf = s.replace('\r\n','\n')
if old_lf in s_lf: s = s_lf.replace(old_lf,new.replace('\r\n','\n')); print('ok')
elif old in s: s=s.replace(old,new); print('ok')
else: print('miss')
# dates/year
s=s.replace('YEAR = "2026"','YEAR = "2025"').replace("YEAR = '2026'","YEAR = '2025'")
s=s.replace('02.02.2026','03.02.2025').replace('17.08.2026','18.08.2025').replace('01.04.2026','01.04.2025').replace('15.08.2026','18.08.2025')
s=s.replace('2026','2025')
open('make_report.py','w',encoding='utf-8').write(s)
print(s.count('2026'))
