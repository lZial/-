"""Обновление полей (оглавления) и сохранение отчёта в формате .doc через Word."""
import os
import sys
import time

import win32com.client as w

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths

BASE = paths.BASE
BUILD = paths.BUILD
BASENAME = paths.BASENAME

DOCX = paths.DOCX
DOC = paths.DOC
PDF = paths.PDF

wdFormatDocument97 = 0
wdFormatPDF = 17
wdFieldTOC = 37


def main():
    app = w.Dispatch("Word.Application")
    app.Visible = False
    app.DisplayAlerts = 0
    d = app.Documents.Open(DOCX)
    time.sleep(2)
    # обновляем оглавление и все поля
    try:
        for i in range(1, d.TablesOfContents.Count + 1):
            d.TablesOfContents(i).Update()
        print("оглавление обновлено, разделов:", d.TablesOfContents.Count, flush=True)
    except Exception as e:
        print("TOC err:", str(e)[:120], flush=True)
    # выравниваем абзацы оглавления: без красной строки, с отступом по уровням
    try:
        for p in d.Range().Paragraphs:
            st = p.Style.NameLocal
            if st.upper().startswith("TOC") or st.upper().startswith("ОГЛАВЛЕНИЕ"):
                p.Format.FirstLineIndent = 0
                if "2" in st:
                    p.Format.LeftIndent = 28.35      # 0,75 см в пунктах
                elif "3" in st:
                    p.Format.LeftIndent = 56.7
                else:
                    p.Format.LeftIndent = 0
                p.Format.SpaceAfter = 0
                p.Format.SpaceBefore = 0
                p.Format.LineSpacingRule = 5         # одинарный
        print("оглавление выровнено", flush=True)
    except Exception as e:
        print("TOC format err:", str(e)[:120], flush=True)
    try:
        d.Fields.Update()
    except Exception as e:
        print("fields err:", str(e)[:120], flush=True)
    try:
        d.Repaginate()
    except Exception:
        pass
    pages = d.ComputeStatistics(2)   # wdStatisticPages
    words = d.ComputeStatistics(0)
    print("страниц:", pages, "слов:", words, flush=True)
    # сохраняем в .doc
    if os.path.exists(DOC):
        os.remove(DOC)
    d.SaveAs2(DOC, FileFormat=wdFormatDocument97)
    print("сохранено:", DOC, os.path.getsize(DOC), flush=True)
    # PDF для проверки
    try:
        d.SaveAs2(PDF, FileFormat=wdFormatPDF)
        print("pdf:", os.path.getsize(PDF), flush=True)
    except Exception as e:
        print("pdf err:", str(e)[:120], flush=True)
    d.Close(SaveChanges=0)
    app.Quit()


if __name__ == "__main__":
    main()
