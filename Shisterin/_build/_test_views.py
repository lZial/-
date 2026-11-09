import os, sys, time
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, capture, say

say('start')
s = Shot()
say('shot ready')
try:
    say('view apply')
    s.app.ViewApply('Использование ресурсов')
    say('applied')
    time.sleep(1.5)
    try:
        s.app.ZoomTimescale(Entire=True)
    except Exception as e:
        say('zoom err', str(e)[:80])
    time.sleep(1.5)
    s.hide()
    time.sleep(0.5)
    say('capture')
    size = capture(s.hwnd, os.path.join(paths.SHOTS, '31_использование_ресурсов.png'))
    say('OK 31', size)
finally:
    try:
        s.app.FileQuit()
    except Exception:
        pass
say('done')
