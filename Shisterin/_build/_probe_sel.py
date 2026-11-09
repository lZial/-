# -*- coding: utf-8 -*-
import os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say

s = Shot()
try:
    s.app.ViewApply("Диаграмма Ганта")
    time.sleep(2.0)
    say("Task8:", s.app.ActiveProject.Tasks.Item(8).Name)
    for field in ("Name", "ID", "Task Name"):
        try:
            s.app.SelectTaskField(8, field, False)
            time.sleep(0.5)
            say(field, "ActiveCell:", repr(s.app.ActiveCell.Text))
        except Exception as e:
            say(field, "ERR", str(e)[:100])
    for meth in ("TaskInformation", "TaskInfo", "TaskDetails"):
        try:
            m = getattr(s.app, meth)
            say(meth, "=> exists", m)
        except Exception as e:
            say(meth, "ERR", str(e)[:60])
    # open dialog via menu
    s.app.SelectTaskField(8, "ID", False)
    time.sleep(0.5)
    say("menu...")
    ok = s.menu("Проект", "Сведения о задаче...")
    say("menu:", ok)
    h, title = s.wait_dialog(10)
    say("dialog:", repr(title))
    if h:
        d = s.dlg_ui(h)
        # read name edit
        try:
            for e in d.descendants(control_type="Edit"):
                v = e.get_value()
                if v:
                    say("  edit:", repr(v)[:60])
        except Exception as e:
            say("edit err", str(e)[:60])
        s.dlg_button(h, "Отмена")
finally:
    try:
        s.app.FileQuit()
    except Exception:
        pass
say("done")
