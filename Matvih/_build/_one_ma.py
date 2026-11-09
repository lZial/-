# -*- coding: utf-8 -*-
"""Съёмка одного представления Матвиха: python _one_ma.py <key>."""
import os
import sys
import time
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, capture, say
import shoot_all as A

OUT = paths.SHOTS
VIEWS = {
    "26": ("Диаграмма Ганта", "26_диаграмма_ганта.png"),
    "27": ("Использование задач", "27_использование_задач.png"),
    "28": ("Сетевой график", "28_сетевой_график.png"),
    "29": ("Календарь", "29_календарь.png"),
    "30": ("Лист ресурсов", "30_лист_ресурсов.png"),
    "31": ("Использование ресурсов", "31_использование_ресурсов.png"),
    "32": ("График ресурсов", "32_график_ресурса.png"),
}


def main():
    key = sys.argv[1]
    view, fname = VIEWS[key]
    s = Shot()
    s.show = lambda: None
    try:
        for _ in range(40):
            if s.wait_ready(3):
                break
            A.close_stray(s)
        A.close_stray(s)
        A.resize(s)
        A.clear_view(s)
        path = os.path.join(OUT, fname)
        try:
            s.app.ViewApply(view)
        except Exception as e:
            say("view fail", view, str(e)[:100])
        time.sleep(2.0)
        if key == "30":
            A.resize(s, 1500, 1200)
            time.sleep(1.0)
        if key == "28":
            try:
                s.app.Zoom(Entire=True)
            except Exception as e:
                say("zoom:", str(e)[:80])
            time.sleep(1.5)
        if key in ("28", "29", "31", "32"):
            size = A.capture_onscreen(s, s.hwnd, path)
        else:
            size = capture(s.hwnd, path)
        say("OK", key, size)
    except Exception as e:
        say("FAIL", key, str(e)[:160])
        traceback.print_exc()
    finally:
        try:
            A.close_stray(s)
        except Exception:
            pass
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
