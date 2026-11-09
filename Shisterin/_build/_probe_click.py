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
    hit = None
    for d in s.mp.descendants(control_type="DataItem"):
        try:
            t = d.window_text()
            if "Создание репозитория" in t:
                hit = d
                say("found:", repr(t)[:60])
                break
        except Exception:
            continue
    if hit is None:
        raise RuntimeError("row not found")
    try:
        hit.click_input()
        say("click_input ok")
    except Exception as e:
        say("click_input ERR", str(e)[:80])
    time.sleep(1.0)
    try:
        say("ActiveCell:", repr(s.app.ActiveCell.Text)[:60])
    except Exception as e:
        say("active err", str(e)[:60])
    s.pre = set()
    keys_to_pid("+{F2}", s.pid)
    h, title = s.wait_dialog(10)
    say("dialog:", repr(title))
    if h:
        capture(h, os.path.join(paths.BUILD, "_dbg_task3.png"))
        s.dlg_button(h, "Отмена")
finally:
    try:
        s.app.FileQuit()
    except Exception:
        pass
say("done")
