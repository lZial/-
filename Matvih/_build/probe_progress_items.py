"""Печать точных имен шаблонов галереи «Ход выполнения»."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reshoot_fixed import Shot, say


def find(root, name):
    for e in root.descendants():
        try:
            if e.window_text().strip() == name:
                return e
        except Exception:
            pass
    return None


def main():
    s = Shot()
    try:
        s.show()
        s.ribbon_tab("Отчет")
        time.sleep(1.0)
        g = find(s.mp, "Ход выполнения")
        g.click_input()
        time.sleep(1.5)
        for e in s.mp.descendants():
            try:
                if getattr(e.element_info, "control_type", "") == "ListItem":
                    say(repr(e.window_text()))
            except Exception:
                pass
        g.click_input()
    finally:
        time.sleep(0.5)
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
