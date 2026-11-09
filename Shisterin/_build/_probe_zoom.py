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
    for name in ('TimescaleStart', 'TimescaleFinish', 'StartDate', 'FinishDate',
                 'Zoom', 'ViewZoom', 'ZoomTimescale', 'ZoomCalendar'):
        try:
            v = getattr(app, name)
            print(name, '=>', v if not callable(v) else 'callable')
        except Exception as e:
            print(name, 'ERR', str(e)[:80])
    # try to set timescale start
    for name, val in (('TimescaleStart', '2025-02-03'), ('TimescaleFinish', '2025-08-18')):
        try:
            setattr(app, name, val)
            print('set', name, 'OK ->', getattr(app, name))
        except Exception as e:
            print('set', name, 'ERR', str(e)[:100])
    app.ViewApply('График ресурсов')
    time.sleep(2)
    try:
        app.ZoomTimescale(Entire=True)
        print('ZoomTimescale ok')
    except Exception as e:
        print('ZoomTimescale ERR', str(e)[:100])
finally:
    try:
        app.FileClose()
    except Exception:
        pass
    try:
        app.Quit()
    except Exception:
        pass
