import os, sys, time
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, capture, say

name = sys.argv[1]
say('start', name)
s = Shot()
try:
    say('apply', name)
    s.app.ViewApply(name)
    say('applied')
    time.sleep(2.0)
    s.hide()
    time.sleep(0.5)
    size = capture(s.hwnd, os.path.join(paths.SHOTS, '32_график_ресурса.png'))
    say('OK', size)
finally:
    try:
        s.app.FileQuit()
    except Exception:
        pass
say('done')
