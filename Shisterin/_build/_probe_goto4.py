# -*- coding: utf-8 -*-
import os, sys, time, ctypes
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say, capture
from winfocus import keys_to_pid
user32 = ctypes.windll.user32

s = Shot()
try:
    s.app.ViewApply("Диаграмма Ганта")
    time.sleep(2.0)
    try:
        s.app.FilterClear()
        say("filter cleared")
    except Exception as e:
        say("filter err", str(e)[:60])
    time.sleep(1.0)
    s.show()
    time.sleep(0.8)
    for tid in ("8", "37"):
        try:
            s.mp.set_focus()
        except Exception:
            pass
        s.pre = set()
        keys_to_pid("{F5}", s.pid)
        h, title = s.wait_dialog(8)
        say("goto dialog:", repr(title))
        if not h:
            raise RuntimeError("no goto")
        try:
            user32.SetForegroundWindow(h)
        except Exception:
            pass
        time.sleep(0.4)
        keys_to_pid("^a", s.pid)
        time.sleep(0.2)
        keys_to_pid(tid, s.pid)
        time.sleep(0.5)
        keys_to_pid("{ENTER}", s.pid)
        time.sleep(1.5)
        try:
            say("tid", tid, "->", repr(s.app.ActiveCell.Task.ID))
        except Exception as e:
            say("active err", str(e)[:80])
finally:
    try:
        s.app.FileQuit()
    except Exception:
        pass
say("done")
