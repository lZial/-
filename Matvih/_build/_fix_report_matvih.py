import sys, re
sys.stdout.reconfigure(encoding='utf-8')
p='make_report2_part2.py'
s=open(p,encoding='utf-8').read()

# dates / EVM / general
repls=[
 ('02.02.2026','03.02.2025'), ('15.08.2026','18.08.2025'), ('17.08.2026','18.08.2025'),
 ('01.04.2026','01.04.2025'), ('13.08.2026','15.08.2025'),
 ('06.05–15.07.2026','06.05–15.07.2025'),
 ('.2026','.2025'),
 ('БСЗР = 2 029 300,00 руб., БСВР = 2 029 300,00 руб., ФСВР = 2 065 220,00 руб.',
  'БСЗР = 1 837 800,00 руб., БСВР = 1 837 800,00 руб., ФСВР = 1 874 080,00 руб.'),
 ('ОКП = БСВР − БСЗР = 0,00 руб., ОПС = БСВР − ФСВР = −35 920,00 руб.',
  'ОКП = БСВР − БСЗР = 0,00 руб., ОПС = БСВР − ФСВР = −36 280,00 руб.'),
 ('ИОКП = БСВР / БСЗР = 1,00 (план по срокам выполняется), ИОПС = БСВР / ФСВР = 0,98 (фактическая стоимость на 2 % выше плановой).',
  'ИОКП = БСВР / БСЗР = 1,00 (план по срокам выполняется), ИОПС = БСВР / ФСВР = 0,98 (фактическая стоимость незначительно выше плановой).'),
 ('MS Project 2024',''),
]
for a,b in repls: s=s.replace(a,b)
s=s.replace('2026 года','2025 года').replace('апреле 2026','апреле 2025').replace('апреля 2026','апреля 2025')
s=re.sub(r'2026(?!\d)', '2025', s)  # any leftover year tokens
s=s.replace('Microsoft Project','файле плана проекта').replace('MS Project','плане проекта')

# stages 4.1
s=re.sub(r'def stages_section\(doc\):.*?heading\(doc, "4\.2 Характеристика этапов", 2\)',
r'''def stages_section(doc):
    heading(doc, "4 Основные этапы и задачи проекта", 1)
    heading(doc, "4.1 Состав этапов проекта", 2)
    para(doc, "Проект разбит на шесть этапов. Внутри этапов выделены рабочие задачи; "
              "отдельно в плане ведётся серия регулярных совещаний команды. "
              "Сроки этапов приведены в таблице ниже.")
    rows = []
    for i, (st, cnt) in enumerate(stage_rows(), 1):
        nm = st["Наименование"].split(". ", 1)[1] if ". " in st["Наименование"] else st["Наименование"]
        rows.append([str(i), nm, str(cnt),
                     days(st["Длительность"]), dmy(st["Начало"]),
                     dmy(st["Окончание"]), hours(st["Трудозатраты"]),
                     money(st["Затраты"])])
    rows.append(["", "Итого по проекту", "", "", "03.02.2025", "18.08.2025", "", money(BUDGET)])
    tcaption(doc, "Этапы проекта")
    table(doc, ["№", "Этап", "Задач", "Длит., дн.", "Начало", "Окончание",
                "Трудозатраты", "Стоимость"], rows, size=9,
          widths=[0.9, 4.6, 1.2, 1.6, 2.2, 2.2, 1.8, 2.0])
    para(doc, "Часть этапов выполняется параллельно, поэтому общая длительность проекта меньше суммы длительностей этапов.")
    heading(doc, "4.2 Характеристика этапов", 2)''', s, count=1, flags=re.S)

# 4.3 list
s=re.sub(r'heading\(doc, "4\.3 Перечень задач проекта", 2\).*?heading\(doc, "4\.4 Вехи проекта", 2\)',
r'''heading(doc, "4.3 Перечень задач проекта", 2)
    para(doc, "Ниже приведён перечень задач проекта. Повторяющиеся совещания в список не включены.")
    for r in TASKS:
        try: rid = int(r["ID"])
        except Exception: continue
        name = r["Наименование"]
        if "Совещание" in name or 68 <= rid <= 96:
            continue
        if r["Уровень"] == "1":
            nm = name.split(". ", 1)[1] if ". " in name else name
            para(doc, "%s. %s" % (rid, nm), indent=0, bold=True)
        else:
            para(doc, "%s. %s" % (rid, name), indent=1.25)
    heading(doc, "4.4 Вехи проекта", 2)''', s, count=1, flags=re.S)

# table captions 7.1/7.2 and other common
s=re.sub(r'para\(doc, "Таблица 7\.1[^"]*".*?\)', 'tcaption(doc, "Загрузка ресурсов проекта")', s)
s=re.sub(r'para\(doc, "Таблица 7\.2[^"]*".*?\)', 'tcaption(doc, "Ход выполнения этапов")', s)
# add tcaption before tables that follow known paragraphs
s=s.replace('              "меры реагирования.")\n    table(doc,','              "меры реагирования.")\n    tcaption(doc, "Реестр рисков проекта")\n    table(doc,')
s=s.replace('(таблица 4.3);', 'приведены в таблице ниже;').replace('(Таблица 4.3);','приведены в таблице ниже;')
# uncaptained common tables
if 'tcaption(doc, "Вехи проекта")' not in s:
    s=s.replace('    table(doc, ["№", "Веха", "Дата"],', '    tcaption(doc, "Вехи проекта")\n    table(doc, ["№", "Веха", "Дата"],')
if 'tcaption(doc, "Загрузка ресурсов проекта")' not in s:
    s=s.replace('    table(doc, ["№", "Ресурс", "Группа", "Трудозатраты", "Стоимость",','    tcaption(doc, "Загрузка ресурсов проекта")\n    table(doc, ["№", "Ресурс", "Группа", "Трудозатраты", "Стоимость",')
if 'tcaption(doc, "Ход выполнения этапов")' not in s:
    s=s.replace('    table(doc, ["№", "Этап", "Начало", "Окончание", "% завершения",','    tcaption(doc, "Ход выполнения этапов")\n    table(doc, ["№", "Этап", "Начало", "Окончание", "% завершения",')
s=re.sub(r'\bтаблиц[а-я]* 4\.\d\b','таблице',s,flags=re.I)
s=re.sub(r'\bТаблица \d+\.\d\b','таблица',s)
s=re.sub(r'Рисунок \d+\.\d','Рисунок',s)  # figure() renumbers; keep word

# tone
s=s.replace('Все шестнадцать практических работ выполнены','Подготовлены основные элементы плана проекта')
s=s.replace('В соответствии с методическими указаниями ','')
s=re.sub(r'практическ\w*\s+работ\w*','работ', s, flags=re.I)
body,sep,tail=s.partition('SOURCES = [')
body=body.replace('учебного проекта ','проекта ').replace('учебный проект','проект')
s=body+sep+tail

open(p,'w',encoding='utf-8').write(s)
# check
b=s.partition('SOURCES = [')[0]
for pat in ['MS Project','Microsoft Project','2026','Таблица \\d+\\.\\d','Рисунок \\d+\\.\\d','методическ']:
    ms=re.findall(pat,b,re.I)
    if ms: print(pat,len(ms))
print('ok')
