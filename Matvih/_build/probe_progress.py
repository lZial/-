"""Список задач с процентом завершения и кнопок вкладки «Формат»."""
import sys
import time

import win32com.client as w

sys.stdout.reconfigure(encoding="utf-8")
app = w.Dispatch("MSProject.Application")
app.Visible = True
app.DisplayAlerts = 0
app.FileOpen(r"D:\UP_NeuralDefects\УП_Матвих.mpp")
time.sleep(2)
pr = app.ActiveProject
for t in pr.Tasks:
    try:
        pc = t.PercentComplete
    except Exception:
        pc = None
    if pc:
        print("ID=%-3s %-55s %3s%% %s - %s" % (
            t.ID, t.Name[:55], pc, t.ActualStart, t.ActualFinish))
app.FileClose(0)
app.FileQuit()
