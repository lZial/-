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
    time.sleep(0.5)
    ok = s.select_task("Создание репозитория", 8)
    say("select_task:", ok)
    time.sleep(0.5)
    try:
        s.app.SelectTaskField(8, "Name", True)
        time.sleep(0.8)
    except Exception as e:
        say("abs sel err", str(e)[:80])
    time.sleep(1.0)
    try:
        say("ActiveCell:", repr(s.app.ActiveCell.Text))
    except Exception as e:
        say("active err", str(e)[:60])
    s.pre = set()
    r = keys_to_pid("+{F2}", s.pid)
    say("shift+F2:", r)
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
