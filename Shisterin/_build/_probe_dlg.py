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
    keys_to_pid("^{HOME}", s.pid)
    time.sleep(0.6)
    for _ in range(7):
        keys_to_pid("{DOWN}", s.pid)
        time.sleep(0.15)
    time.sleep(0.8)
    s.pre = set()
    keys_to_pid("+{F2}", s.pid)
    h, title = s.wait_dialog(10)
    say("dialog:", repr(title))
    if h:
        d = s.dlg_ui(h)
        for e in d.descendants():
            try:
                ct = getattr(e.element_info, "control_type", "")
                t = e.window_text()
                v = ""
                try:
                    v = str(e.get_value())
                except Exception:
                    pass
                if t or v:
                    say("  ", ct, repr(t[:50]), "|", repr(v[:50]))
            except Exception:
                pass
        say("cap:", capture(h, os.path.join(paths.BUILD, "_dbg_task.png")))
        s.dlg_button(h, "Отмена")
finally:
    try:
        s.app.FileQuit()
    except Exception:
        pass
say("done")
