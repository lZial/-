"""Патч утилит make_report.py: 12pt, интервалы 0, заголовки слева, сквозная нумерация."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')

NEW = r'''# сквозные счётчики (сбрасываются при формировании документа)
_FIG_NO = [0]
_TAB_NO = [0]


def reset_counters():
    _FIG_NO[0] = 0
    _TAB_NO[0] = 0


def next_fig():
    _FIG_NO[0] += 1
    return _FIG_NO[0]


def next_tab():
    _TAB_NO[0] += 1
    return _TAB_NO[0]


def para(doc, text="", size=12, bold=False, italic=False, align="justify",
         indent=1.25, spacing=1.5, before=0, after=0, caps=False, keep=False):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = {"justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
                    "center": WD_ALIGN_PARAGRAPH.CENTER,
                    "left": WD_ALIGN_PARAGRAPH.LEFT,
                    "right": WD_ALIGN_PARAGRAPH.RIGHT}[align]
    if indent is not None:
        pf.first_line_indent = Cm(indent)
    pf.line_spacing = spacing
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    if keep:
        pf.keep_with_next = True
    if text:
        set_run_font(p.add_run(text), size, bold, italic, caps)
    return p


def heading(doc, text, level=1):
    """Заголовок раздела/подраздела: по левому краю с абзацным отступом."""
    p = para(doc, text, size=12, bold=True, align="left",
             indent=1.25, spacing=1.5, before=0, after=0, keep=True)
    p.style = doc.styles["Heading %d" % level]
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.first_line_indent = Cm(1.25)
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    for r in p.runs:
        set_run_font(r, 12, True, False, caps=False)
    return p


def figure(doc, filename, caption, width_cm=16.0, number=True):
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

def patch(path):
    s = open(path, encoding='utf-8').read()
    if 'reset_counters' in s and 'tcaption' in s and 'size=12, bold=False' in s:
        print('skip', path); return
    # replace from def para( to end of figure(
    import re
    pat = re.compile(r'def para\(doc,.*?def table\(doc, headers, rows, widths=None, size=12\):', re.S)
    # easier: find markers
    a = s.find('def para(')
    b = s.find('def table(doc, headers, rows, widths=None')
    if a<0 or b<0:
        print('MISS markers', path, a,b); return
    s = s[:a] + NEW + '\n\n\n' + s[b:]
    # setup_styles
    s2 = s
    a = s.find('def setup_styles(doc):')
    b = s.find('\n# ----', a)
    if b<0: b = s.find('\ndef title_page', a)
    if a>=0 and b>a:
        s = s[:a] + r'''def setup_styles(doc):
    reset_counters()
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(12)
    rpr = st.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts"); rpr.append(rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), "Times New Roman")
    pf = st.paragraph_format
    pf.first_line_indent = Cm(1.25)
    pf.line_spacing = 1.5
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for lvl in (1, 2, 3):
        h = doc.styles["Heading %d" % lvl]
        h.font.name = "Times New Roman"
        h.font.size = Pt(12)
        h.font.bold = True
        h.font.color.rgb = RGBColor(0, 0, 0)
        hp = h.paragraph_format
        hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        hp.first_line_indent = Cm(1.25)
        hp.space_before = Pt(0)
        hp.space_after = Pt(0)
''' + s[b:]
    # table trailing para spacing
    s = s.replace('para(doc, "", indent=0, spacing=1.0, after=6)\n    return t',
                  'para(doc, "", indent=0, spacing=1.0, before=0, after=0)\n    return t')
    # add tcaption after page_break if missing
    if 'def tcaption' not in s:
        s = s.replace('def page_break(doc):\n    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)',
                      '''def page_break(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def tcaption(doc, text):
    """Подпись таблицы сверху, сквозная нумерация."""
    for sep in (" – ", " - ", "—"):
        if sep in text:
            text = text.split(sep, 1)[1]
            break
    if text.lower().startswith("таблица"):
        parts = text.split(None, 2)
        text = parts[2] if len(parts) > 2 else text
    return para(doc, "Таблица %d – %s" % (next_tab(), text.strip()),
                size=12, align="left", indent=0, spacing=1.0, before=0, after=0, keep=True)''')
    open(path,'w',encoding='utf-8').write(s)
    print('patched', path)

for p in sys.argv[1:]:
    patch(p)
