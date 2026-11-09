import sys, time
sys.stdout.reconfigure(encoding='utf-8')
import win32com.client as w
app = w.DispatchEx('MSProject.Application')
app.Visible = False
app.DisplayAlerts = 0
try:
    app.FileOpen(r'D:\UP_MobileBank\УП_Шистерин.mpp')
    time.sleep(3)
    try:
        views = app.Views
        print('count', views.Count)
        for i in range(1, views.Count + 1):
            v = views.Item(i)
            try:
                print(i, v.Name)
            except Exception as e:
                print(i, 'err', e)
    except Exception as e:
        print('views err', e)
finally:
    try:
        app.FileClose()
    except Exception:
        pass
    try:
        app.Quit()
    except Exception:
        pass
