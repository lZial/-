import io
import sys

sys.stdout.reconfigure(encoding='utf-8')
p = 'make_report2_part2.py'
s = open(p, encoding='utf-8').read()
start = s.index('def appendix_a(doc):')
end = s.index('# ----------------------------------------------------------------- сборка')
new = '''def appendix_a(doc):
    heading(doc, "Приложение А", 1)
    para(doc, "Отчёт «Обзор проекта»", align="center", indent=0, bold=True)
    figure(doc, "43_отчет_обзор_проекта.png",
          "Рисунок А.1 – Отчёт «Обзор проекта», сформированный в MS Project",
          width_cm=23.0)
    para(doc, "Отчёт сформирован в Microsoft Project 2024 на статусную дату "
              "01.04.2026: завершены этапы 1 и 2, этап 3 выполнен на 19 %, "
              "отклонений по срокам нет (SV = 0), перерасход CV = –195 160 руб. "
              "при CPI = 0,91.")
    page_break(doc)


def appendix_b(doc):
    heading(doc, "Приложение Б", 1)
    para(doc, "Отчёт «Стоимость проекта»", align="center", indent=0, bold=True)
    figure(doc, "44_отчет_обзор_затрат.png",
          "Рисунок Б.1 – Отчёт «Стоимость проекта» (обзор затрат), "
          "сформированный в MS Project", width_cm=23.0)
    para(doc, "Наибольшая доля бюджета приходится на этап 3 «Формирование "
              "датасета и обучение модели» (31,6 %), далее следуют интеграция "
              "(18,9 %) и тестирование (15,0 %). Стоимость материальных "
              "ресурсов включена в стоимость соответствующих задач.")
    page_break(doc)


def appendix_v(doc):
    heading(doc, "Приложение В", 1)
    para(doc, "Отчёт «Загрузка ресурсов»", align="center", indent=0, bold=True)
    figure(doc, "45_отчет_обзор_ресурсов.png",
          "Рисунок В.1 – Отчёт «Загрузка ресурсов» (обзор ресурсов), "
          "сформированный в MS Project", width_cm=23.0)
    para(doc, "Основная нагрузка приходится на ML-инженера (836 часов), "
              "тестировщика (484 часа) и CV-инженера (308 часов); пиковая "
              "загрузка ML-инженера достигает 400 % в апреле 2026 г. "
              "Выравнивание выполнено в ручном режиме, сроки проекта не "
              "изменены.")
    page_break(doc)


def appendix_g(doc):
    heading(doc, "Приложение Г", 1)
    para(doc, "Отчёт «Ход выполнения»", align="center", indent=0, bold=True)
    figure(doc, "46_отчет_ход_выполнения.png",
          "Рисунок Г.1 – Отчёт «Ход выполнения» (шаблон «Отчет о вехах»), "
          "сформированный в MS Project", width_cm=23.0)
    para(doc, "К статусной дате 01.04.2026 завершены этапы 1 и 2, этап 3 "
              "выполнен на 19 %. Отклонение по срокам отсутствует, по "
              "стоимости зафиксировано CV = –195 160 руб.; прогнозная "
              "стоимость завершения EAC = 7 284 384 руб.")


def appendix_d(doc):
    heading(doc, "Приложение Д", 1)
    para(doc, "Диаграмма Ганта проекта", align="center", indent=0, bold=True)
    para(doc, "")
    para(doc, "Диаграмма Ганта отражает календарный план проекта. Для "
              "наглядности применён фильтр «Суммарные задачи» и масштаб "
              "«Весь проект»: на диаграмме видны шесть этапов, их "
              "длительности и взаимное расположение во времени. Этапы "
              "3–6 выполняются частично параллельно, поэтому их полосы "
              "перекрываются. Детальный перечень задач с датами и связями "
              "приведён в таблице 4.2, вехи проекта — в таблице 4.3.")
    figure(doc, "26_диаграмма_ганта.png",
           "Рисунок Д.1 – Диаграмма Ганта проекта «%s»" % THEME,
           width_cm=16.5)


def _set_section(sec, landscape):
    if landscape:
        sec.orientation = WD_ORIENT.LANDSCAPE
        sec.page_width = Cm(29.7)
        sec.page_height = Cm(21.0)
    else:
        sec.orientation = WD_ORIENT.PORTRAIT
        sec.page_width = Cm(21.0)
        sec.page_height = Cm(29.7)
    sec.left_margin = Cm(3)
    sec.right_margin = Cm(1.5)
    sec.top_margin = Cm(2)
    sec.bottom_margin = Cm(2)
    sec.header_distance = Cm(1.2)
    sec.footer_distance = Cm(1.2)


def appendices(doc):
    sec = doc.add_section(WD_SECTION.NEW_PAGE)
    _set_section(sec, True)
    appendix_a(doc)
    appendix_b(doc)
    appendix_v(doc)
    appendix_g(doc)
    sec2 = doc.add_section(WD_SECTION.NEW_PAGE)
    _set_section(sec2, False)
    appendix_d(doc)


'''
s = s[:start] + new + s[end:]
open(p, 'w', encoding='utf-8').write(s)
print('patched')
