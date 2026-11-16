# -*- coding: utf-8 -*-
"""Приведение УП_Шистерин.docx к выбранному оформлению.

1. Нумерация разделов (включая Введение/Заключение/Список источников)
2. Подписи рисунков: "Рисунок N – Название"
3. Приложения: цифровая нумерация (Приложение 1..5)
4. Авто-оглавление
5. Пункты списка источников пронумерованы (уже есть)
6. Размеры заголовков как в примере А: H1 14 pt, H2 13 pt
"""
import copy
import os
import re
import shutil
import sys

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

sys.stdout.reconfigure(encoding="utf-8")

DOCX = r"D:\UP_MobileBank\УП_Шистерин.docx"
BAK = DOCX + ".bak_before_format_fix"
if not os.path.exists(BAK):
    shutil.copy2(DOCX, BAK)
    print("backup", BAK)

FIG_TITLES = {
    1: "Этапы гибкой методологии Agile (Scrum)",
    2: "Окно «Сведения о проекте»",
    3: "Диаграмма Ганта проекта",
    4: "Таблица задач проекта",
    5: "Окно «Сведения о задаче»",
    6: "Вкладка «Дополнительно» окна «Сведения о задаче»",
    7: "Сетевой график проекта",
    8: "Диаграмма Ганта проекта",
    9: "Представление «Диаграмма предшествования»",
    10: "Представление «Лист ресурсов»",
    11: "Диалоговое окно «Назначение ресурсов»",
    12: "Таблица «Затраты»",
    13: "Представление «Использование задач»",
    14: "Диалоговое окно «Выравнивание загрузки ресурсов»",
    15: "Представление «Использование ресурсов»",
    16: "Представление «График ресурсов»",
    17: "Сводная таблица проекта",
    18: "Окно «Статистика проекта»",
    19: "Диалоговое окно «Мастер диаграмм Ганта»",
    20: "Диалоговое окно «Стили отрезков»",
    21: "Диалоговое окно «Печать»",
    22: "Диалоговое окно «Параметры страницы»",
    23: "Диалоговое окно «Изменение рабочего времени»",
    24: "Диалоговое окно «Заметки о задаче»",
    25: "Диалоговое окно «Сведения о повторяющейся задаче»",
    26: "Диалоговое окно «Параметры» (вкладка «Расписание»)",
    27: "Диалоговое окно «Стили текста»",
    28: "Диалоговое окно «Изменение рабочего времени» для ресурса",
    29: "Окно «Сведения о задаче»",
    30: "Представление «Лист ресурсов»",
    31: "Представление «Использование ресурсов»",
    32: "Представление «Календарь»",
    33: "Представление «Использование задач»",
    34: "Диалоговое окно «Сортировка»",
    35: "Диалоговое окно «Другие фильтры»",
    36: "Диалоговое окно «Сетка»",
    37: "Окно «Заметки» задачи с описанием решения и риска",
    38: "Диалоговое окно «Вставка гиперссылки»",
    39: "Диалоговое окно «Другие фильтры»",
    40: "Диалоговое окно «Сохранение базового плана»",
    41: "Диалоговое окно «Обновление задач»",
    42: "Таблица «Трудозатраты»",
    43: "Таблица «Трудозатраты»",
    44: "Диалоговое окно «Наглядные отчёты»",
    45: "Таблица «Трудозатраты»",
    46: "Таблица норм затрат ресурса (эксперимент 2)",
    47: "Окно «Статистика проекта» после эксперимента 2",
    48: "Отчёт «Обзор проекта»",
    49: "Отчёт «Затраты задач»",
    50: "Отчёт «Затраты ресурсов»",
    51: "Отчёт «Ход выполнения»",
    52: "Диаграмма Ганта проекта",
}

doc = Document(DOCX)


def set_para_text(p, text):
    if not p.runs:
        p.add_run(text)
    else:
        p.runs[0].text = text
        for r in p.runs[1:]:
            r.text = ""


# 6. heading sizes like A
for style_name, size in [("Heading 1", 14), ("Heading 2", 13), ("Heading 3", 13)]:
    try:
        st = doc.styles[style_name]
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.name = "Times New Roman"
    except Exception as e:
        print("style err", style_name, e)
print("heading styles updated")


# 1. renumber headings: Введение -> 1 Введение, N... -> N+1...
def renum_heading(text):
    if text == "Введение":
        return "1 Введение"
    m = re.match(r'^(\d+(?:\.\d+)*)(\s+)(.*)$', text)
    if not m:
        return text
    nums = m.group(1).split('.')
    nums[0] = str(int(nums[0]) + 1)
    return '.'.join(nums) + m.group(2) + m.group(3)

heading_changes = 0
for p in doc.paragraphs:
    st = p.style.name if p.style else ""
    if not (st.startswith("Heading") or st.startswith("Заголовок")):
        continue
    t = (p.text or "").strip()
    if not t:
        continue
    # appendices handled separately
    if t.startswith("Приложение"):
        continue
    new = renum_heading(t)
    if new != t:
        set_para_text(p, new)
        heading_changes += 1
        print("H:", t, "->", new)
print("heading renumbered:", heading_changes)


# 2. figure captions
fig_n = 0
for p in doc.paragraphs:
    t = (p.text or "").strip()
    m = re.match(r'^Рисунок\s+(\d+)$', t)
    if not m:
        continue
    n = int(m.group(1))
    title = FIG_TITLES.get(n, "")
    if title:
        set_para_text(p, f"Рисунок {n} – {title}")
    else:
        set_para_text(p, f"Рисунок {n}")
    # center caption
    try:
        p.alignment = 1  # CENTER
    except Exception:
        pass
    fig_n += 1
print("figure captions updated:", fig_n)


# 3. appendices -> numeric like B
app_map = {"А": 1, "Б": 2, "В": 3, "Г": 4, "Д": 5}
app_changes = 0
for p in doc.paragraphs:
    st = p.style.name if p.style else ""
    t = (p.text or "").strip()
    if not (st.startswith("Heading") or st.startswith("Заголовок")):
        continue
    m = re.match(r'^Приложение\s+([АБВГДA-E])$', t)
    if m:
        letter = m.group(1)
        num = app_map.get(letter)
        if num:
            set_para_text(p, f"Приложение {num}")
            app_changes += 1
print("appendices updated:", app_changes)


# 4. auto TOC: replace "СОДЕРЖАНИЕ" paragraph with title + TOC field
for i, p in enumerate(doc.paragraphs):
    t = (p.text or "").strip().upper()
    if t == "СОДЕРЖАНИЕ":
        # keep paragraph as title
        set_para_text(p, "СОДЕРЖАНИЕ")
        try:
            p.alignment = 1
        except Exception:
            pass
        # insert TOC field in a new paragraph after it
        toc_p = OxmlElement('w:p')
        r = OxmlElement('w:r')
        fldChar1 = OxmlElement('w:fldChar')
        fldChar1.set(qn('w:fldCharType'), 'begin')
        instr = OxmlElement('w:instrText')
        instr.set(qn('xml:space'), 'preserve')
        instr.text = ' TOC \\o "1-3" \\h \\z \\u '
        fldCharSep = OxmlElement('w:fldChar')
        fldCharSep.set(qn('w:fldCharType'), 'separate')
        r2 = OxmlElement('w:r')
        t2 = OxmlElement('w:t')
        t2.text = 'Обновите оглавление (ПКМ → Обновить поле) при открытии документа в Word.'
        r2.append(t2)
        fldChar2 = OxmlElement('w:fldChar')
        fldChar2.set(qn('w:fldCharType'), 'end')
        r.append(fldChar1)
        r.append(instr)
        r.append(fldCharSep)
        toc_p.append(r)
        toc_p.append(r2)
        r3 = OxmlElement('w:r')
        r3.append(fldChar2)
        toc_p.append(r3)
        p._p.addnext(toc_p)
        print("TOC field inserted after para", i)
        break

doc.save(DOCX)
print("saved", DOCX)
