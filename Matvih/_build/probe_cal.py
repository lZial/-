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
cal = pr.BaseCalendars.Item(1)
print("календарь:", repr(cal.Name))
for e in cal.Exceptions:
    print("   искл:", repr(e.Name), e.Start, e.Finish)
print("начало:", pr.ProjectSummaryTask.Start, "окончание:", pr.ProjectSummaryTask.Finish)
try:
    print("базовый план:", pr.ProjectSummaryTask.Baseline10SaveDate)
except Exception as ex:
    print("bpd:", str(ex)[:100])
app.FileClose(0)
app.FileQuit()
