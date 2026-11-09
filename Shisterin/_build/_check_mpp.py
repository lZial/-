import sys, os, time
sys.stdout.reconfigure(encoding='utf-8')
import win32com.client as w
app = w.DispatchEx("MSProject.Application")
app.Visible = True
app.DisplayAlerts = 0
try:
    app.FileOpen(r'D:\UP_MobileBank\УП_Шистерин.mpp')
    time.sleep(3)
    p = app.ActiveProject
    print('start', p.ProjectStart, 'finish', p.ProjectFinish)
    print('status date', p.StatusDate)
    print('tasks', p.Tasks.Count, 'resources', p.Resources.Count)
    print('calc', p.Calculation, 'current date', p.CurrentDate)
    print('default start', p.DefaultStartTime)
    print('cost', p.ProjectCost)
finally:
    try:
        app.FileClose()
    except Exception as e:
        print('close err', e)
    try:
        app.Quit()
    except Exception:
        pass
