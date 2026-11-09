"""Дамп кнопок вкладки «Формат диаграммы Ганта»."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say


def main():
    s = Shot()
    s.show = lambda: None
    try:
        s.app.ViewApply("Диаграмма Ганта")
        s.app.SelectTaskField(29, "Name", False)
        time.sleep(1.0)
        say("tabs:", [t.window_text() for t in s.mp.descendants(control_type="TabItem")])
        s.ribbon_tab("Формат диаграммы Ганта")
        time.sleep(1.5)
        seen = set()
        for b in s.mp.descendants(control_type="Button"):
            try:
                t = b.window_text().strip()
                if t and t not in seen:
                    seen.add(t)
                    say("Button", repr(t))
            except Exception:
                pass
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
