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
    s.pre = set()
    keys_to_pid("{F5}", s.pid)
    h, title = s.wait_dialog(8)
    say("goto dialog:", repr(title))
    if not h:
        raise RuntimeError("no goto")
    d = s.dlg_ui(h)
    edits = list(d.descendants(control_type="Edit"))
    say("edits:", len(edits))
    edits[0].set_edit_text("8")
    time.sleep(0.4)
    s.dlg_button(h, "ОК")
    time.sleep(1.5)
    try:
        say("ActiveCell:", repr(s.app.ActiveCell.Text)[:60])
        say("Task:", repr(s.app.ActiveCell.Task.Name)[:60])
    except Exception as e:
        say("active err", str(e)[:80])
    s.pre = set()
    keys_to_pid("+{F2}", s.pid)
    h2, t2 = s.wait_dialog(10)
    say("task dlg:", repr(t2))
    if h2:
        capture(h2, os.path.join(paths.BUILD, "_dbg_task4.png"))
        s.dlg_button(h2, "Отмена")
finally:
    try:
        s.app.FileQuit()
    except Exception:
        pass
say("done")
