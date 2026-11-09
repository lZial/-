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
    for name, fn in (
        ("SelectRow", lambda: s.app.SelectRow(8, False)),
        ("SelectTaskField Name True", lambda: s.app.SelectTaskField(8, "Name", True)),
        ("SelectTaskField ID True", lambda: s.app.SelectTaskField(8, "ID", True)),
    ):
        try:
            fn()
            time.sleep(0.8)
            try:
                tn = s.app.ActiveCell.Task.Name
            except Exception as e:
                tn = "ERR " + str(e)[:40]
            say(name, "->", repr(tn)[:60], "| cell", repr(s.app.ActiveCell.Text)[:40])
        except Exception as e:
            say(name, "ERR", str(e)[:80])
    # now open dialog
    s.pre = set()
    keys_to_pid("+{F2}", s.pid)
    h, title = s.wait_dialog(10)
    say("dialog:", repr(title))
    if h:
        capture(h, os.path.join(paths.BUILD, "_dbg_task2.png"))
        s.dlg_button(h, "Отмена")
finally:
    try:
        s.app.FileQuit()
    except Exception:
        pass
say("done")
