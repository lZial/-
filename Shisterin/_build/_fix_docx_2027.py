# -*- coding: utf-8 -*-
"""Обновление УП_Шистерин.docx: даты 2027, актуальные числа/EV, эксперимент.
Годы изданий книг в библиографии не трогаем (меняем только дату обращения)."""
import glob, os, re, shutil, sys
from docx import Document

sys.stdout.reconfigure(encoding="utf-8")

# locate docx
cands = [p for p in glob.glob(r"D:\UP_MobileBank\*.docx")
         if os.path.basename(p).startswith("УП_") and "эксперимент" not in p and "bak" not in p]
if not cands:
    cands = [p for p in glob.glob(r"D:\UP_MobileBank\УП_Шистерин.docx")]
path = cands[0]
bak = path + ".bak_before_2027fix2"
if not os.path.exists(bak):
    shutil.copy2(path, bak)
    print("backup", bak)

doc = Document(path)

# detect bibliography start (paragraph index in doc.paragraphs)
bib_start = None
for i, p in enumerate(doc.paragraphs):
    t = (p.text or "").strip()
    if t.startswith("Список использованных источников") or t.startswith("СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ"):
        bib_start = i
        break
# fallback: first numbered bib item
if bib_start is None:
    for i, p in enumerate(doc.paragraphs):
        if (p.text or "").strip().startswith("1. Аньшин"):
            bib_start = i
            break

def fmt_money(x):
    # 3041440 -> 3 041 440
    s = f"{int(round(x)):,}".replace(",", " ")
    return s

# helper to set paragraph text preserving first run style roughly
def set_para_text(p, text):
    if not p.runs:
        p.add_run(text)
        return
    p.runs[0].text = text
    for r in p.runs[1:]:
        r.text = ""

# targeted full-paragraph replacements by key substrings (applied anywhere including tables)
EXACT_REWRITES = [
    # EV analysis paragraph (base) - replace old wrong numbers
    ("Анализ отчётов показал, что к статусной дате завершены этапы 1 и 2 (100 %), этап 3 выполнен на 19 %, остальные этапы ещё не начаты. Освоенный объём соответствует плановому (SV = 0), однако фактические затраты превышают освоенный объём на 195 160 руб. (CV = –195 160 руб., CPI = 0,91), что связано с повышением ставки ключевого исполнителя. Прогнозная стоимость завершения (EAC) составляет 7 284 384 руб. при бюджете 3 041 440 руб., поэтому рекомендовано пересмотреть ставки и усилить контроль стоимости.",
     "Анализ отчётов показал, что к статусной дате завершены этапы 1 и 2 (100 %), этап 3 выполнен на 14 %, остальные этапы ещё не начаты. По базовому плану освоенный объём превышает плановый (BCWP 864 784 руб., BCWS 812 560 руб., SV = +52 224 руб.) и превышает фактические затраты (ACWP 812 560 руб., CV = +52 224 руб.), что свидетельствует о небольшом опережении графика и экономии затрат. Индексы CPI и SPI равны 1,064. Прогнозная стоимость завершения (EAC) составляет 2 857 769 руб. при бюджете (BAC) 3 041 440 руб., отклонение по завершении (VAC) — +183 671 руб., индекс TCPI — 0,977."),
    # EV mid-section (old base-as-bad in 4.14 text)
    ("Отклонение по календарному плану (ОКП, SV = БСВР − БСРЗ) равно нулю, что свидетельствует о выполнении работ точно в срок. Отклонение по стоимости (ОПС, CV = БСВР − ФСВР) составило −195 160 руб. — фактические затраты превысили освоенный объём, что обусловлено применением повышенной ставки «Мобильный разработчик» с 01.04.2025 (см. приложение В).",
     "Отклонение по календарному плану (ОКП, SV = БСВР − БСРЗ) составило +52 224 руб. (БСВР 864 784 руб., БСРЗ 812 560 руб.), что свидетельствует о небольшом опережении графика. Отклонение по стоимости (ОПС, CV = БСВР − ФСВР) составило +52 224 руб. (ФСВР 812 560 руб.), то есть фактические затраты ниже освоенного объёма."),
    ("Индекс отклонения от стоимости (ИОС, CPI = БСВР / ФСВР) равен 0,91, индекс отклонения от календарного плана (ИОП, SPI = БСВР / БСРЗ) — 1,00. Значение ИОС ниже единицы указывает на перерасход средств, значение ИОП, равное единице, — на соответствие календарному плану. Предварительная оценка затрат по завершении (ПОПЗ, EAC = ФСВР + (БПЗ − БСВР) / ИОС) составила 7 284 384 руб. при бюджете по завершении (БПЗ, BAC) 3 041 440 руб.; отклонение по завершении (ОПЗ, VAC = БПЗ − ПОПЗ) равно −687 384 руб. Относительное отклонение по стоимости (ООС, CV % = ОПС / БСВР × 100) составило −10,4 %.",
     "Индекс отклонения от стоимости (ИОС, CPI = БСВР / ФСВР) равен 1,064, индекс отклонения от календарного плана (ИОП, SPI = БСВР / БСРЗ) — 1,064. Значения индексов выше единицы указывают на опережение графика и экономию средств. Предварительная оценка затрат по завершении (ПОПЗ, EAC = BAC / CPI) составила 2 857 769 руб. при бюджете по завершении (БПЗ, BAC) 3 041 440 руб.; отклонение по завершении (ОПЗ, VAC = БПЗ − ПОПЗ) равно +183 671 руб. Индекс выполнения плана (TCPI = (BAC − БСВР) / (BAC − ФСВР)) составляет 0,977."),
    # corrupted experiment paragraph
    ("В этом эксперименте, когда разработчик и тестировщик не могли работать все пять рабочих дней. Часть задач заняла больше: календарь сдвинул срок окончания всего проекта примерно на пять недель, а сумма затрат выросла на 1 047 200 руб. (почти 15,9 %). Но вносился это вручную, сам по себе только в том самом плане появился оптимизирован.",
     "В экспериментальном плане учтены ограничения апреля 2027 года: для мобильного разработчика пятницы апреля сделаны нерабочими, для тестировщика — сокращёнными (09:00–13:00), а с 01.04.2027 повышена ставка мобильного разработчика с 1 000 до 1 500 руб./ч (сверхурочные — с 1 500 до 2 250 руб./ч). В результате стоимость проекта увеличилась с 3 041 440 до 3 415 440 руб., то есть на 374 000 руб. (около 12,3 %), при сохранении сроков окончания проекта."),
    # experiment 2 line in text (may appear differently)
]

# also fix common wrong fragments if full match fails
FRAG_REWRITES = [
    ("этап 3 выполнен на 19 %", "этап 3 выполнен на 14 %"),
    ("этап 3 выполнен на 19%", "этап 3 выполнен на 14%"),
    ("3 416 560", "3 415 440"),
    ("3416560", "3415440"),
    ("375 120", "374 000"),
    ("375120", "374000"),
    ("1 047 200", "374 000"),
    ("1047200", "374000"),
    ("15,9 %", "12,3 %"),
    ("15,9%", "12,3%"),
    ("7 284 384", "2 857 769"),
    ("7284384", "2857769"),
    ("−687 384", "+183 671"),
    ("-687 384", "+183 671"),
    ("−195 160", "+52 224"),
    ("-195 160", "+52 224"),
    ("195 160", "52 224"),
    ("(SV = 0)", "(SV = +52 224 руб.)"),
    ("SV = 0", "SV = +52 224 руб."),
    ("CPI = 0,91", "CPI = 1,064"),
    ("CPI = 0.91", "CPI = 1,064"),
    ("SPI = 1,00", "SPI = 1,064"),
    ("SPI — 1,00", "SPI — 1,064"),
]

# specific date/range replacements for stage descriptions to match 2027 facts
DATE_REWRITES = [
    ("(02.02–20.02.2025)", "(03.02–23.02.2027)"),
    ("(02.02-20.02.2025)", "(03.02-23.02.2027)"),
    ("(20.02–23.03.2025)", "(22.02–24.03.2027)"),
    ("(20.02-23.03.2025)", "(22.02-24.03.2027)"),
    ("(23.03–07.05.2025)", "(24.03–07.05.2027)"),
    ("(23.03-07.05.2025)", "(24.03-07.05.2027)"),
    ("(06.05–16.06.2025)", "(07.05–16.06.2027)"),
    ("(06.05-16.06.2025)", "(07.05-16.06.2027)"),
    ("(06.05–15.07.2025)", "(07.05–16.07.2027)"),
    ("(06.05-15.07.2025)", "(07.05-16.07.2027)"),
    ("(06.02–18.08.2025)", "(08.02–17.08.2027)"),
    ("(06.02-18.08.2025)", "(08.02-17.08.2027)"),
    ("03.02.2025", "03.02.2027"),
    ("18.08.2025", "17.08.2027"),
    ("15.08.2025", "16.08.2027"),
    ("06.02.2025", "08.02.2027"),
    ("14.08.2025", "16.08.2027"),
    ("01.04.2025", "01.04.2027"),
    ("1.04.2025", "01.04.2027"),
    ("Самара, 2025", "Самара, 2027"),
    ("2025 года", "2027 года"),
    ("в 2025 году", "в 2027 году"),
    ("с 03.02.2025 по 18.08.2025", "с 03.02.2027 по 17.08.2027"),
    ("с 06.02.2025 по 14.08.2025", "с 08.02.2027 по 16.08.2027"),
]

# regex for remaining dd.mm.2025 and dd.mm-dd.mm.2025 in non-bibliography text
DATE_RE = re.compile(r'(\b\d{1,2}\.\d{1,2}\.)(2025)\b')
RANGE_RE = re.compile(r'(\b\d{1,2}\.\d{1,2})[–-](\d{1,2}\.\d{1,2}\.)(2025)\b')


def transform_text(text, in_bib):
    if not text:
        return text
    orig = text
    # always fix access date
    text = text.replace("дата обращения: 01.04.2025", "дата обращения: 01.04.2027")
    text = text.replace("дата обращения: 1.04.2025", "дата обращения: 01.04.2027")
    if in_bib:
        return text
    # exact rewrites
    for a, b in EXACT_REWRITES:
        if a in text:
            text = text.replace(a, b)
    # fragments
    for a, b in FRAG_REWRITES:
        text = text.replace(a, b)
    # known dates/phrases
    for a, b in DATE_REWRITES:
        text = text.replace(a, b)
    # generic dd.mm.2025 -> dd.mm.2027 (but avoid if it's clearly a book year like " 2025. -" unlikely in dd.mm form)
    # ranges first
    text = RANGE_RE.sub(lambda m: m.group(1) + "–" + m.group(2) + "2027", text)
    text = DATE_RE.sub(lambda m: m.group(1) + "2027", text)
    # any leftover isolated " 2025" year tokens in narrative that look like project year? be careful
    # fix specific: "Отчёты сформированы на статусную дату 01.04.2025" handled, "Установлена дата отчётности (статусная дата) 01.04.2025" handled
    return text

# apply to paragraphs
changes = 0
for i, p in enumerate(doc.paragraphs):
    in_bib = bib_start is not None and i >= bib_start
    old = p.text or ""
    new = transform_text(old, in_bib)
    if new != old:
        # preserve style by editing runs carefully: simplest set full text on first run
        set_para_text(p, new)
        changes += 1

# apply to tables
tchanges = 0
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                # table cells - treat as non-bib unless text looks like bib; safer: apply but protect book years
                # detect bib-like: contains "(дата обращения" with URL pattern or starts with digit.
                old = p.text or ""
                in_bib_cell = False
                if "дата обращения" in old and "URL:" in old:
                    in_bib_cell = True
                new = transform_text(old, in_bib_cell)
                if new != old:
                    set_para_text(p, new)
                    tchanges += 1

print("paragraph changes", changes, "table cell para changes", tchanges)

# extra pass: fix corrupted paragraph by searching for garbled marker
for p in doc.paragraphs:
    t = p.text or ""
    if t.startswith("?") and "15,9" in t or ("эксперимент" in t.lower() and "1 047 200" in t):
        set_para_text(p, "В экспериментальном плане учтены ограничения апреля 2027 года: для мобильного разработчика пятницы апреля сделаны нерабочими, для тестировщика — сокращёнными (09:00–13:00), а с 01.04.2027 повышена ставка мобильного разработчика с 1 000 до 1 500 руб./ч (сверхурочные — с 1 500 до 2 250 руб./ч). В результате стоимость проекта увеличилась с 3 041 440 до 3 415 440 руб., то есть на 374 000 руб. (около 12,3 %), при сохранении сроков окончания проекта.")
        print("fixed corrupted exp paragraph")

out = path
doc.save(out)
print("saved", out)
