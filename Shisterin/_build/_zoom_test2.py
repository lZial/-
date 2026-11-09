# -*- coding: utf-8 -*-
import os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reshoot_fixed import Shot, say

s = Shot()
try:
    s.app.ViewApply("Сетевой график")
    time.sleep(2)
    say("menu Вид/Масштаб")
    ok = s.menu("Вид", "Масштаб...")
    say("menu:", ok)
    h, title = s.wait_dialog(10)
    say("dialog:", repr(title))
    if h:
        d = s.dlg_ui(h)
        if d is not None:
            for e in d.descendants():
                try:
                    ct = getattr(e.element_info, "control_type", "")
                    if ct in ("RadioButton", "Button", "ListItem", "ComboBox", "CheckBox"):
                        say("  el", ct, repr(e.window_text().strip()[:60]))
                except Exception:
                    pass
        s.dlg_button(h, "Отмена")
finally:
    try:
        s.app.FileQuit()
    except Exception:
        pass
say("done")
