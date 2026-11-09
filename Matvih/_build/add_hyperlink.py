"""Создаёт реестр рисков и привязывает его гиперссылкой к задаче 50."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
import win32com.client as w
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

DOC = os.path.join(paths.BASE, "Реестр_рисков_проекта.docx")


def make_doc():
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(12)
    h = d.add_paragraph()
    r = h.add_run("Реестр рисков проекта системы технического зрения")
    r.bold = True
    r.font.size = Pt(14)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rows = [
        ("Изменение требований промышленной безопасности", "40 %", "120 000",
         "Согласование регламентов со службой качества, буфер 2 дня"),
        ("Несогласованность протоколов обмена с АСУ ТП", "35 %", "95 000",
         "Еженедельный семинар с интеграторами"),
        ("Дефицит ML-инженеров", "30 %", "150 000",
         "Резерв из команды CV-инженеров, буфер 3 дня"),
        ("Переобучение модели", "45 %", "180 000",
         "Расширение датасета, кросс-валидация, буфер 4 дня"),
        ("Массовые дефекты при функциональном тестировании", "50 %", "220 000",
         "Буфер 5 дней в этапе исправления дефектов"),
    ]
    t = d.add_table(rows=1, cols=4)
    t.style = "Table Grid"
    for i, name in enumerate(("Риск", "Вероятность", "Потери, руб.", "Меры")):
        t.rows[0].cells[i].text = name
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = val
    d.save(DOC)
    print("создан", DOC)


def link():
    app = w.Dispatch("MSProject.Application")
    app.Visible = False
    app.DisplayAlerts = 0
    app.FileOpen(paths.MPP)
    p = app.ActiveProject
    t = p.Tasks.Item(50)
    t.Hyperlink = "Реестр рисков проекта"
    t.HyperlinkAddress = DOC
    print("задача:", t.Name, "| ссылка:", t.Hyperlink, "|", t.HyperlinkAddress)
    p.SaveAs(paths.MPP)
    app.FileClose(0)
    app.FileQuit()


if __name__ == "__main__":
    if not os.path.exists(DOC):
        make_doc()
    link()
