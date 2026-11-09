# -*- coding: utf-8 -*-
import sys, time
sys.stdout.reconfigure(encoding='utf-8')
import win32com.client as w
app = w.DispatchEx('MSProject.Application')
app.Visible = False
app.DisplayAlerts = 0
try:
    app.FileOpen(r'D:\UP_MobileBank\УП_Шистерин.mpp')
    time.sleep(3)
    p = app.ActiveProject
    for i in range(1, 25):
        try:
            t = p.Tasks.Item(i)
            print(i, t.ID, repr(t.Name)[:60], t.Start, t.Finish)
        except Exception as e:
            print(i, 'ERR', str(e)[:60])
finally:
    try:
        app.FileClose()
    except Exception:
        pass
    try:
        app.Quit()
    except Exception:
        pass
