# -*- coding: utf-8 -*-
import os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say, capture
from winfocus import keys_to_pid

s = Shot()
try:
    s.app.ViewApply("Диаграмма Ганта")
    time.sleep(2.0)
    s.show()
    time.sleep(0.8)
    try:
        s.mp.set_focus()
    except Exception:
        pass
    for key in ("{F5}", "^{g}"):
        s.pre = set()
        say("send", key, keys_to_pid(key, s.pid))
        h, title = s.wait_dialog(5)
        say("  dialog:", repr(title))
        if h:
            capture(h, os.path.join(paths.BUILD, "_goto.png"))
            s.dlg_button(h, "Отмена")
            break
finally:
    try:
        s.app.FileQuit()
    except Exception:
        pass
say("done")
