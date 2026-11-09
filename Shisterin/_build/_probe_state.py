# -*- coding: utf-8 -*-
import sys, time
sys.stdout.reconfigure(encoding='utf-8')
import win32com.client as w
app = w.DispatchEx('MSProject.Application')
app.Visible = True
app.DisplayAlerts = 0
try:
    app.FileOpen(r'D:\UP_MobileBank\УП_Шистерин.mpp')
    time.sleep(4)
    p = app.ActiveProject
    print('name', p.Name, 'readonly', p.ReadOnly, 'tasks', p.Tasks.Count)
    print('windows', app.Windows.Count)
    for i in range(1, app.Windows.Count + 1):
        win = app.Windows.Item(i)
        print(' win', i, win.Caption, 'proj', win.Project.Name)
    try:
        print('activeview', app.ActiveView.Name)
    except Exception as e:
        print('activeview ERR', e)
    for name in ('Диаграмма Ганта', 'Лист ресурсов'):
        try:
            app.ViewApply(name)
            time.sleep(1.5)
            print('ViewApply', name, 'OK; activeview', app.ActiveView.Name)
        except Exception as e:
            print('ViewApply', name, 'ERR', str(e)[:100])
    try:
        app.SelectTaskField(8, 'Name', False)
        print('sel ok; ActiveCell.Task', app.ActiveCell.Task.Name)
    except Exception as e:
        print('sel ERR', str(e)[:140])
finally:
    try:
        app.FileClose()
    except Exception as e:
        print('close', e)
    try:
        app.Quit()
    except Exception:
        pass
