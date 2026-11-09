# -*- coding: utf-8 -*-
import os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say
from winfocus import keys_to_pid

s = Shot()
try:
    s.app.ViewApply("Диаграмма Ганта")
    time.sleep(2.0)
    s.show()
    time.sleep(0.8)
    try:
        s.mp.set_focus()
    except Exception as e:
        say("focus err", str(e)[:60])
    time.sleep(0.5)
    say("home:", keys_to_pid("{HOME}", s.pid))
    time.sleep(0.6)
    for _ in range(7):
        keys_to_pid("{DOWN}", s.pid)
        time.sleep(0.15)
    time.sleep(0.8)
    try:
        say("ActiveCell:", repr(s.app.ActiveCell.Text))
    except Exception as e:
        say("active err", str(e)[:60])
    s.pre = set()
    say("F2:", keys_to_pid("+{F2}", s.pid))
    h, title = s.wait_dialog(10)
    say("dialog:", repr(title))
    if h:
        d = s.dlg_ui(h)
        for e in d.descendants(control_type="Edit"):
            try:
                v = e.get_value()
                if v:
                    say("  edit:", repr(v)[:70])
            except Exception:
                pass
        s.dlg_button(h, "Отмена")
finally:
    try:
        s.app.FileQuit()
    except Exception:
        pass
say("done")
