import os, sys, time
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, capture, say

say('start')
s = Shot()
try:
    for name in ('График ресурса', 'Диаграмма использования ресурсов', 'Использование ресурсов'):
        try:
            say('try', name)
            s.app.ViewApply(name)
            say('applied', name)
            time.sleep(1.5)
            s.app.ZoomTimescale(Entire=True)
            time.sleep(1.5)
            s.hide()
            time.sleep(0.5)
            size = capture(s.hwnd, os.path.join(paths.SHOTS, '32_график_ресурса.png'))
            say('OK 32', name, size)
            break
        except Exception as e:
            say('fail', name, str(e)[:90])
finally:
    try:
        s.app.FileQuit()
    except Exception:
        pass
say('done')
