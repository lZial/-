# -*- coding: utf-8 -*-
import sys, time
sys.stdout.reconfigure(encoding='utf-8')
import win32com.client as w
app = w.DispatchEx('MSProject.Application')
app.Visible = False
app.DisplayAlerts = 0
try:
    app.FileOpen(r'D:\UP_NeuralDefects\УП_Матвих.mpp')
    time.sleep(3)
    p = app.ActiveProject
    print('start', p.ProjectStart)
    print('finish', p.ProjectFinish)
    print('status', p.StatusDate)
    for prop in ('CurrentDate',):
        try:
            print(prop, getattr(p, prop))
        except Exception as e:
            print(prop, 'ERR', e)
    try:
        print('app.CurrentDate', app.CurrentDate)
    except Exception as e:
        print('app.CurrentDate ERR', e)
    # try setting project current date
    try:
        p.CurrentDate = '2025-04-01'
        print('set CurrentDate OK ->', p.CurrentDate)
    except Exception as e:
        print('set CurrentDate ERR', e)
    try:
        app.CurrentDate = '2025-04-01'
        print('set app.CurrentDate OK ->', app.CurrentDate)
    except Exception as e:
        print('set app.CurrentDate ERR', e)
finally:
    try:
        app.FileClose()
    except Exception as e:
        print('close', e)
    try:
        app.Quit()
    except Exception:
        pass
