"""
Формирование отчёта по практическим работам (МДК.03.02 «Управление проектами»).
Тема - «Разработка нейросети для распознавания дефектов на производстве».
"""
import json
import os
import sys

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths

BASE = paths.BASE
SHOTS = paths.SHOTS
BUILD = paths.BUILD
BASENAME = paths.BASENAME

THEME = "Разработка нейросети для распознавания дефектов на производстве"

try:
    cfg = paths.load_config()
except Exception:
    cfg = {}
FIO = cfg.get("fio") or "Фамилия Имя Отчество"
GROUP = cfg.get("group") or "________"
STUDENT = cfg.get("student") or FIO
CITY = cfg.get("city") or "Самара"
YEAR = cfg.get("year") or "2025"
# имя файла по требованию МУ: «УП_фамилия»
SURNAME = paths.surname()
OUT_DOCX = paths.DOCX

COLLEGE = ("Автономная некоммерческая организация\n"
           "профессиональная образовательная организация\n"
           "«Самарский колледж цифровой экономики и предпринимательства «МИР»\n"
           "(АНО ПОО Колледж «МИР»)")
DISCIPLINE = "МДК.03.02 «Управление проектами»"
SPECIALTY = "09.02.07 «Информационные системы и программирование»"

# ----------------------------------------------------------------- утилиты
def set_run_font(run, size=14, bold=False, italic=False, caps=False):
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(a), "Times New Roman")
    if caps:
        el = OxmlElement("w:caps")
        el.set(qn("w:val"), "1")
        rpr.append(el)


# сквозные счётчики (сбрасываются при формировании документа)
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
    """Заголовок раздела/подраздела: по левому краю с абзацным отступом; до/после — пустая строка при наличии текста."""
    # если перед заголовком есть текст — одна пропущенная строка
    if doc.paragraphs:
        prev = doc.paragraphs[-1]
        prev_st = prev.style.name if prev.style else ''
        prev_has_drawing = bool(prev._element.xpath('.//w:drawing') or prev._element.xpath('.//w:pict'))
        if (prev.text.strip() or prev_has_drawing) and 'Heading' not in prev_st:
            blank0 = doc.add_paragraph()
            bpf0 = blank0.paragraph_format
            bpf0.first_line_indent = Cm(0)
            bpf0.space_before = Pt(0)
            bpf0.space_after = Pt(0)
            bpf0.line_spacing = 1.5
            set_run_font(blank0.add_run(""), 12, False)
    p = para(doc, text, size=12, bold=True, align="left",
             indent=1.25, spacing=1.5, before=0, after=0, keep=False)
    p.style = doc.styles["Heading %d" % level]
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.first_line_indent = Cm(1.25)
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    for r in p.runs:
        set_run_font(r, 12, True, False, caps=False)
    # одна пропущенная строка после названия главы/подглавы
    blank = doc.add_paragraph()
    bpf = blank.paragraph_format
    bpf.first_line_indent = Cm(0)
    bpf.space_before = Pt(0)
    bpf.space_after = Pt(0)
    bpf.line_spacing = 1.5
    br = blank.add_run("")
    set_run_font(br, 12, False)
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
    if number:
        cap = "Рисунок %d" % next_fig()
    else:
        cap = caption
    cp = para(doc, cap, size=12, align="center", indent=0, spacing=1.0, before=0, after=0)
    for r in cp.runs:
        r.italic = False


def table(doc, headers, rows, widths=None, size=12):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.autofit = widths is None
    if widths is not None:
        tblPr = t._tbl.tblPr
        layout = OxmlElement("w:tblLayout")
        layout.set(qn("w:type"), "fixed")
        tblPr.append(layout)
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = ""
        p = c.paragraphs[0]
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_run_font(p.add_run(h), size, True)
        if widths is not None:
            c.width = Cm(widths[i])
    # повторять строку заголовка на каждой странице
    trPr = t.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement("w:tblHeader")
    th.set(qn("w:val"), "true")
    trPr.append(th)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            set_run_font(p.add_run(str(val)), size)
            if widths is not None:
                cells[i].width = Cm(widths[i])
    para(doc, "", indent=0, spacing=1.0, before=0, after=0)
    return t


def page_break(doc):
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
                size=12, align="left", indent=0, spacing=1.0, before=0, after=0, keep=False)


def add_field(paragraph, instr):
    r = paragraph.add_run()
    fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = instr
    fs = OxmlElement("w:fldChar"); fs.set(qn("w:fldCharType"), "separate")
    fe = OxmlElement("w:fldChar"); fs.set(qn("w:fldCharType"), "end")
    r._r.append(fc); r._r.append(it); r._r.append(fs); r._r.append(fe)
    return r


def setup_section(doc):
    s = doc.sections[0]
    s.page_width = Cm(21)
    s.page_height = Cm(29.7)
    s.left_margin = Cm(3)
    s.right_margin = Cm(1.5)
    s.top_margin = Cm(2)
    s.bottom_margin = Cm(2)
    s.header_distance = Cm(1.2)
    s.footer_distance = Cm(1.2)
    s.different_first_page_header_footer = True
    # колонтитулы (кроме титульного листа)
    hp = s.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    hp.paragraph_format.first_line_indent = Cm(0)
    hp.paragraph_format.line_spacing = 1.0
    set_run_font(hp.add_run("Тема: «%s». %s" % (THEME, STUDENT)), 12)
    fp = s.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fp.paragraph_format.first_line_indent = Cm(0)
    fp.paragraph_format.line_spacing = 1.0
    set_run_font(add_field(fp, "PAGE"), 12)
    return s


def setup_styles(doc):
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

# ----------------------------------------------------------------- отчёт
def build():
    doc = Document()
    setup_styles(doc)
    setup_section(doc)

    # ---------------- ТИТУЛЬНЫЙ ЛИСТ
    for _ in range(2):
        para(doc, "", indent=0)
    for line in COLLEGE.split("\n"):
        para(doc, line, align="center", indent=0, spacing=1.0)
    para(doc, "", indent=0, spacing=1.5)
    para(doc, "", indent=0, spacing=1.5)
    para(doc, "ОТЧЁТ", align="center", indent=0, bold=True, spacing=1.5)
    para(doc, "по практическим работам", align="center", indent=0, spacing=1.5)
    para(doc, "по дисциплине %s" % DISCIPLINE, align="center", indent=0, spacing=1.5)
    para(doc, "Специальность %s" % SPECIALTY, align="center", indent=0, spacing=1.5)
    para(doc, "", indent=0, spacing=1.5)
    para(doc, "Тема проекта:", align="center", indent=0, spacing=1.5)
    para(doc, "«%s»" % THEME, align="center", indent=0, bold=True, spacing=1.5)
    para(doc, "Модель жизненного цикла: итерационная (Iterative)", align="center", indent=0, spacing=1.5)
    for _ in range(3):
        para(doc, "", indent=0, spacing=1.5)
    para(doc, "Выполнил(а): студент(ка) группы %s" % GROUP, align="right", indent=0, spacing=1.5)
    para(doc, FIO, align="right", indent=0, spacing=1.5)
    para(doc, "Проверил(а): ______________________", align="right", indent=0, spacing=1.5)
    para(doc, "", indent=0, spacing=1.5)
    para(doc, "%s, %s" % (CITY, YEAR), align="center", indent=0, spacing=1.5)

    page_break(doc)

    # ---------------- СОДЕРЖАНИЕ
    heading(doc, "Содержание", 1)
    tp = doc.add_paragraph()
    tp.paragraph_format.first_line_indent = Cm(0)
    tp.paragraph_format.line_spacing = 1.5
    add_field(tp, 'TOC \\o "1-2" \\h \\z \\u')
    page_break(doc)

    # ---------------- ЗАДАНИЕ К ПРОЕКТУ
    heading(doc, "Задание к проекту и описание предметной области", 1)
    para(doc, "Учебный проект выполняется в соответствии с приложением к методическим "
              "указаниям по организации и выполнению практических занятий по дисциплине "
              "%s (специальность %s). Тема проекта выбрана из перечня тем "
              "нового набора 2025 года: «%s», что соответствует итерационной модели "
              "жизненного цикла разработки (Iterative Model)." % (DISCIPLINE, SPECIALTY, THEME))
    para(doc, "Цель проекта: разработка плана создания нейросетевой системы "
              "распознавания дефектов на производстве в среде программе планирования "
              "(программе планирования) и его практическая отработка по шестнадцати практическим "
              "работам в одном файле проекта.")
    para(doc, "Задачи проекта: проанализировать задачи, решаемые разрабатываемой "
              "информационной системой в выбранной предметной области; обосновать "
              "преимущества и недостатки выбранной модели жизненного цикла; выбрать "
              "способ планирования; выполнить декомпозицию работ и построить "
              "структурную модель проекта; создать план проекта с задачами, "
              "ограничениями, длительностями и связями (не менее двух различных типов "
              "связей); настроить календарь с учётом праздничных дней; задать "
              "временные ограничения, ресурсы и их стоимость; выполнить выравнивание "
              "загрузки ресурсов; сохранить базовый план; провести сопровождение "
              "проекта и анализ по методике освоенного объёма; проанализировать риски; "
              "сформировать и напечатать отчёты.")
    para(doc, "Объём проекта: 97 задач (6 сводных задач этапов, сводная задача "
              "«Совещание», 62 рабочие задачи и 28 повторяющихся совещаний), "
              "18 ресурсов (14 трудовых и 4 материальных). Длительность проекта — "
              "с 02.02.2025 по 17.08.2025 (около 6,5 месяцев), что превышает "
              "минимально допустимый срок в один месяц. Плановый бюджет проекта — "
              "6 597 000 руб.")
    para(doc, "Способ планирования выбран «от даты начала проекта»: дата начала "
              "02.02.2025 (понедельник) задана в диалоговом окне «Сведения о проекте», "
              "дата окончания рассчитана программой автоматически.")
    para(doc, "Модель жизненного цикла. Для системы распознавания дефектов выбрана "
              "итерационная модель (Iterative Model). Её преимущества: раннее "
              "получение работающего прототипа, возможность дообучения модели по "
              "мере накопления данных, управление неопределённостью машинного "
              "обучения, прозрачность промежуточных результатов. Недостатки: "
              "сложность точного планирования числа итераций, риск разрастания "
              "требований, необходимость постоянной коммуникации между "
              "дата-сайентистами, инженерами АСУ ТП и технологами. В настоящем "
              "проекте данные особенности учтены за счёт жёсткого планирования в "
              "программе планирования: декомпозиции до 62 рабочих задач, шести этапов-вех, "
              "регламента испытаний и контроля изменений через настраиваемые поля "
              "рисков.")
    para(doc, "Предметная область. Нейросетевая система распознавания дефектов — "
              "это информационная система технического зрения, которая получает "
              "изображения продукции с камер на конвейере, выполняет детекцию и "
              "классификацию поверхностных и внутренних дефектов (трещины, сколы, "
              "вмятины, царапины, поры, нарушения покрытия), визуализирует "
              "локализацию дефекта и передаёт результат оператору и в систему "
              "отбраковки. Система интегрируется с промышленной АСУ ТП, "
              "MES-системой предприятия, конвейерной линией и системой отбраковки, "
              "а также ведёт базу истории дефектов.")
    para(doc, "Нормативные ограничения предметной области: ГОСТ Р 56920-2016 "
              "«Системная инженерия. Требования к разработке и документированию "
              "программного обеспечения», ГОСТ Р 54869-2011 «Проектный менеджмент. "
              "Требования к управлению проектом», требования промышленной "
              "безопасности и внутренние регламенты службы качества предприятия. "
              "Отдельная работа посвящена проверке соответствия этим требованиям.")
    page_break(doc)

    # ---------------- ОСНОВНАЯ ЧАСТЬ
    heading(doc, "Основная часть. Описание этапов разработки проекта", 1)
    para(doc, "Все практические работы выполнены в едином файле проекта "
              "«%s.mpp» (программе планирования 2024). Ниже приведён "
              "пошаговый отчёт о выполнении работ с иллюстрациями." % BASENAME)

    works = WORKS
    for w in works:
        heading(doc, w["title"], 2)
        for t in w["text"]:
            para(doc, t)
        for img, cap in w["images"]:
            figure(doc, img, cap)

    # ---------------- СПИСОК ИСТОЧНИКОВ
    page_break(doc)
    heading(doc, "Список использованных источников", 1)
    para(doc, "Основные:", bold=True, indent=1.25, align="left")
    src_main = [
        "Беликова, И. П. Основы управления проектами : учебное пособие : [16+] / "
        "И. П. Беликова, О. Н. Федиско ; Ставропольский государственный аграрный "
        "университет. – Ставрополь : Ставропольский государственный аграрный "
        "университет (СтГАУ), 2020. – 112 с. : ил. – Режим доступа: по подписке. – "
        "URL: https://biblioclub.ru/index.php?page=book&id=614085",
        "Арсеньев, Ю. Н. Управление проектами, программами : учебник : в 2 томах : "
        "[16+] / Ю. Н. Арсеньев, Т. Ю. Давыдова ; под ред. Ю. Н. Арсеньева. – "
        "Москва ; Берлин : Директ-Медиа, 2021. – Том 1. Методология проектов. – "
        "473 с. : ил., табл. – Режим доступа: по подписке. – URL: "
        "https://biblioclub.ru/index.php?page=book&id=600625",
        "Арсеньев, Ю. Н. Управление проектами, программами : учебник : в 2 томах : "
        "[16+] / Ю. Н. Арсеньев, Т. Ю. Давыдова ; под науч. ред. Ю. Н. Арсеньева. – "
        "Москва ; Берлин : Директ-Медиа, 2021. – Том 2. Реализация проектов. – "
        "565 с. : ил., табл. – Режим доступа: по подписке. – URL: "
        "https://biblioclub.ru/index.php?page=book&id=601692",
        "Преображенская, Т. В. Управление проектами : учебное пособие : [16+] / "
        "Т. В. Преображенская, М. Ш. Муртазина, А. Алетдинова ; Новосибирский "
        "государственный технический университет. – Новосибирск : НГТУ, 2018. – "
        "123 с. : ил., табл. – Режим доступа: по подписке. – URL: "
        "https://biblioclub.ru/index.php?page=book&id=574957",
        "Крумина, К. В. Управление проектами : учебное пособие : [16+] / "
        "К. В. Крумина, С. Г. Полковникова ; Омский государственный технический "
        "университет. – Омск : ОмГТУ, 2020. – 118 с. : ил., табл., схем. – "
        "Режим доступа: по подписке. – URL: "
        "https://biblioclub.ru/index.php?page=book&id=683233",
    ]
    for i, s in enumerate(src_main, 1):
        para(doc, "%d. %s" % (i, s), indent=0, align="justify")
    para(doc, "Дополнительные:", bold=True, indent=1.25, align="left")
    src_add = [
        "Никитаева, А. Ю. Проектный менеджмент : учебное пособие / А. Ю. Никитаева – "
        "Ростов-на-Дону ; Таганрог : Южный федеральный университет, 2018 – 189 с. : "
        "ил. – Режим доступа: по подписке – URL: "
        "https://biblioclub.ru/index.php?page=book&id=499893",
        "Мандель, Б. Р. Основы проектной деятельности: учебное пособие для "
        "обучающихся в системе СПО : [12+] / Б. Р. Мандель. – Изд. 2-е, стер. – "
        "Москва ; Берлин : Директ-Медиа, 2021. – 294 с. : ил., табл., схем. – "
        "Режим доступа: по подписке – URL: "
        "https://biblioclub.ru/index.php?page=book&id=616196",
        "Документация программе планирования 2024: справка по диаграмме Ганта, "
        "управлению ресурсами, выравниванию загрузки, методике освоенного объёма "
        "и формированию отчётов. – URL: https://support.microsoft.com/ru-ru/project",
    ]
    for i, s in enumerate(src_add, len(src_main) + 1):
        para(doc, "%d. %s" % (i, s), indent=0, align="justify")
    para(doc, "Информационные ресурсы:", bold=True, indent=1.25, align="left")
    for s in ["http://www.pmexpert.ru/library – библиотека фирмы PM Expert",
              "http://www.pmpractice.ru/knowledgebase – база знаний по управлению "
              "проектами группы компаний «Проектная ПРАКТИКА»",
              "http://www.strategplann.ru – сайт «Стратегическое планирование и "
              "стратегическое управление»"]:
        para(doc, "– " + s, indent=0, align="justify")

    # ---------------- ПРИЛОЖЕНИЕ
    page_break(doc)
    heading(doc, "Приложение", 1)
    para(doc, "Приложение А. Сводный перечень задач проекта", bold=True, align="center")
    rows = []
    try:
        import csv
        with open(os.path.join(BUILD, "tasks.tsv"), encoding="utf-8") as f:
            rd = csv.DictReader(f, delimiter="\t")
            for r in rd:
                rows.append([r["ID"], r["Уровень"], r["Наименование"], r["Длительность"],
                             str(r["Начало"])[:10], str(r["Окончание"])[:10],
                             r["Предшественники"], r["Ресурсы"], r["Затраты"]])
    except Exception as e:
        para(doc, "Ошибка чтения дампа: %s" % e)
    table(doc, ["№", "Ур.", "Наименование задачи", "Длит.", "Начало", "Окончание",
                "Предш.", "Ресурсы", "Затраты"], rows, size=9)
    para(doc, "Приложение Б. Сводный перечень ресурсов проекта", bold=True, align="center")
    rrows = []
    try:
        import csv
        with open(os.path.join(BUILD, "resources.tsv"), encoding="utf-8") as f:
            rd = csv.DictReader(f, delimiter="\t")
            for r in rd:
                rrows.append([r["Имя"], r["Инициалы"], r["Группа"],
                              {"0": "трудовой", "1": "материальный", "2": "затрат"}.get(r["Тип"], r["Тип"]),
                              r["Макс. единиц"], r["Стандартная ставка"],
                              r["Ставка сверхурочных"], r["Трудозатраты"], r["Затраты"]])
    except Exception as e:
        para(doc, "Ошибка чтения дампа: %s" % e)
    table(doc, ["Ресурс", "Инициалы", "Группа", "Тип", "Макс. ед.", "Ставка",
                "Сверхурочные", "Трудозатраты", "Затраты"], rrows, size=9)
    para(doc, "Приложение В. Результаты экспериментов с копией плана проекта",
         bold=True, align="center")
    para(doc, "В соответствии с приложением к методическим указаниям была создана копия "
              "плана проекта (файл «%s_эксперимент.mpp») и проведена "
              "серия экспериментов по изучению свойств назначений, ресурсов и задач."
              % BASENAME)
    table(doc, ["Эксперимент", "Параметры", "Срок проекта", "Бюджет проекта"],
          [["Исходный план", "—", "17.08.2025", "6 597 000 руб."],
           ["Эксперимент 1. Персональные календари",
            "«Мобильный разработчик» — пятницы апреля 2025 г. нерабочие; "
            "«Тестировщик» — пятницы апреля 2025 г. половина рабочего дня (09:00–13:00)",
            "17.08.2025 (изменений нет)", "6 597 000 руб. (изменений нет)"],
           ["Эксперимент 1б. Перевод 21 задачи в тип «Фиксированный объём ресурсов»",
            "Мобильный разработчик [200%], Тестировщик [150%]", "17.08.2025",
            "6 597 000 руб."],
           ["Эксперимент 2. Изменение ставки ресурса",
            "Ставка «Мобильный разработчик» повышена с 2 200 до 3 600 руб/ч "
            "(сверхурочная — с 3 500 до 5 600 руб/ч) с 01.04.2025 до конца проекта",
            "17.08.2025", "7 621 800 руб. (+1 024 800 руб.)"]], size=11)
    para(doc, "Выводы по экспериментам. Изменение персонального календаря ресурса "
              "при типе задачи «Фиксированная длительность» не изменяет ни "
              "продолжительность, ни стоимость проекта: объём работ задачи "
              "определяется длительностью и числом назначенных единиц, а календарь "
              "ресурса влияет лишь на распределение загрузки по календарю. Перевод "
              "21 задачи в тип «Фиксированный объём ресурсов» также не изменил срок, "
              "поскольку у критических задач имеется запас времени, поглощающий "
              "недостающую производительность. Изменение ставки ресурса с 01.04.2025 "
              "оказалось ощутимым: бюджет проекта вырос на 1 024 800 руб. (15,5 %), "
              "что подтверждает необходимость контроля стоимости ресурсов на "
              "протяжении всего проекта.")
    para(doc, "Приложение Г. Основные показатели проекта", bold=True, align="center")
    table(doc, ["Показатель", "Значение"],
          [["Начало проекта", "02.02.2025"],
           ["Окончание проекта", "17.08.2025"],
           ["Длительность проекта", "196 календарных дней (около 6,5 месяцев)"],
           ["Количество задач", "68 (6 сводных этапов, 62 рабочие задачи)"],
           ["Количество вех", "6"],
           ["Количество ресурсов", "18 (14 трудовых, 4 материальных)"],
           ["Плановый бюджет", "6 597 000 руб."],
           ["Бюджет экспериментальной копии", "7 621 800 руб."],
           ["БСЗР (BCWS) на 01.04.2025", "1 873 000 руб."],
           ["БСВР (BCWP) на 01.04.2025", "1 873 000 руб."],
           ["ФСВР (ACWP) на 01.04.2025", "2 068 160 руб."],
           ["Отклонение от календарного плана (SV)", "0 руб."],
           ["Отклонение по стоимости (CV)", "–195 160 руб."],
           ["Индекс отклонения по стоимости (CPI)", "0,91"],
           ["Индекс отклонения от календарного плана (SPI)", "1,00"],
           ["Предварительная оценка затрат по завершении (EAC)", "7 284 384 руб."],
           ["Отклонение по завершению (VAC)", "–687 384 руб."],
           ["Показатель эффективности выполнения (TCPI)", "1,04"],
           ["Стоимость этапов 1…6", "573 000; 1 071 200; 2 081 600; 1 244 000; "
            "992 000; 635 200 руб."],
           ["Использованные типы связей", "Окончание-начало, Начало-начало, "
            "Начало-окончание, Окончание-окончание"],
           ["Запаздывание (lag) в плане", "+2 дня (связь «Начало-начало»), "
            "+2 дня (связь «Начало-окончание»), +1 день (связь «Окончание-окончание»)"],
           ["Виды временных ограничений", "Фиксированное начало, Начало не ранее, "
            "Окончание не позднее, Фиксированное окончание"],
           ["Праздничные дни (нерабочие)", "12 дней: 1, 2, 5, 6, 7, 8 января; "
            "23 февраля; 8 марта; 1 и 9 мая; 12 июня; 4 ноября 2025 г."]], size=11)

    doc.save(OUT_DOCX)
    print("saved:", OUT_DOCX, os.path.getsize(OUT_DOCX))


# ----------------------------------------------------------------- тексты работ
from works import WORKS  # noqa: E402,F401  (тексты 16 практических работ)


if __name__ == "__main__":
    build()
