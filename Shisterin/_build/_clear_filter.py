# -*- coding: utf-8 -*-
import sys, time
sys.stdout.reconfigure(encoding='utf-8')
import win32com.client as w
app = w.DispatchEx('MSProject.Application')
app.Visible = True
app.DisplayAlerts = 0
path = sys.argv[1]
try:
    app.FileOpen(path)
    time.sleep(4)
    app.ViewApply('Диаграмма Ганта')
    time.sleep(1.5)
    try:
        app.FilterClear()
    except Exception as e:
        print('filter', e)
    app.OutlineShowAllTasks()
    time.sleep(0.8)
    app.FileSave()
    print('saved clean', path)
finally:
    try:
        app.FileClose()
    except Exception as e:
        print('close', e)
    try:
        app.Quit()
    except Exception:
        pass
