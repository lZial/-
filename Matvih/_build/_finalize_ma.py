import os, sys, time
import win32com.client as w
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
DOCX, DOC, PDF = paths.DOCX, paths.DOC, paths.PDF
wdFormatDocument97, wdFormatPDF = 0, 17
app = None; d = None
try:
    app = w.DispatchEx("Word.Application")
    app.Visible = False
    app.DisplayAlerts = 0
    d = app.Documents.Open(DOCX)
    time.sleep(2)
    try:
        for i in range(1, d.TablesOfContents.Count + 1):
            d.TablesOfContents(i).Update()
        for p in d.Range().Paragraphs:
            st = p.Style.NameLocal
            if st.upper().startswith("TOC") or st.upper().startswith("ОГЛАВЛЕНИЕ"):
                p.Format.FirstLineIndent = 0
                if "2" in st: p.Format.LeftIndent = 28.35
                elif "3" in st: p.Format.LeftIndent = 56.7
                else: p.Format.LeftIndent = 0
                p.Format.SpaceAfter = 0; p.Format.SpaceBefore = 0; p.Format.LineSpacingRule = 5
    except Exception as e: print('toc err', e)
    try: d.Fields.Update()
    except Exception as e: print('fld err', e)
    try: d.Repaginate()
    except: pass
    try:
        pages = d.ComputeStatistics(2); words = d.ComputeStatistics(0)
        print("страниц:", pages, "слов:", words, flush=True)
    except Exception as e: print('stats err', e)
    if os.path.exists(DOC): os.remove(DOC)
    d.SaveAs2(DOC, FileFormat=wdFormatDocument97)
    print("сохранено:", DOC, os.path.getsize(DOC), flush=True)
    d.SaveAs2(PDF, FileFormat=wdFormatPDF)
    print("pdf:", os.path.getsize(PDF), flush=True)
    d.Close(SaveChanges=0)
except Exception as e:
    print('ERR', e); import traceback; traceback.print_exc()
finally:
    try:
        if app: app.Quit()
    except: pass
time.sleep(1)
os.system('taskkill /F /IM WINWORD.EXE >nul 2>&1')
