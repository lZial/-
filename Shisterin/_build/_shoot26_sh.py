# -*- coding: utf-8 -*-
"""Снимок 26 (диаграмма Ганта, сводные задачи) без ZoomTimescale."""
import os
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, capture, say
from shoot_gantt import stitch

user32 = __import__("ctypes").windll.user32
SWP_NOZORDER = 0x0004


def zoom_entire(s):
    if not s.menu("Вид", "Масштаб..."):
        raise RuntimeError("нет меню Вид/Масштаб")
    h, title = s.wait_dialog(10)
    if not h:
        raise RuntimeError("нет диалога Масштаб")
    d = s.dlg_ui(h)
    done = False
    if d is not None:
        for e in d.descendants(control_type="RadioButton"):
            try:
                if "роект" in e.window_text():
                    e.select()
                    done = True
                    break
            except Exception:
                pass
    say("  «Весь проект»:", done)
    time.sleep(0.5)
    s.dlg_button(h, "ОК")
    time.sleep(1.8)


def main():
    s = Shot()
    try:
        user32.SetWindowPos(s.hwnd, 0, -4000, -4000, 1500, 1000, SWP_NOZORDER)
        time.sleep(1.5)
        s.app.ViewApply("Диаграмма Ганта")
        time.sleep(2.0)
        try:
            s.app.FilterApply("Суммарные задачи", False)
            say("фильтр: Суммарные задачи")
        except Exception as e:
            say("фильтр:", str(e)[:70])
        time.sleep(1.0)
        zoom_entire(s)
        time.sleep(2.0)
        try:
            s.app.TimelineShow = False
        except Exception as e:
            say("timeline:", str(e)[:70])
        time.sleep(1.5)
        say("OK 26", capture(s.hwnd, os.path.join(paths.SHOTS, "26_диаграмма_ганта.png")))
    finally:
        try:
            os.remove(os.path.join(paths.SHOTS, "_gantt_raw.png"))
        except Exception:
            pass
        try:
            s.close_all()
        except Exception:
            pass
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
