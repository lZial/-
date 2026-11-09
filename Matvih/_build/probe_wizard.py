"""Поиск элементов «Мастер диаграмм», «Стили текста», «Масштаб» в окне."""
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
        time.sleep(1.0)
        s.ribbon_tab("Формат диаграммы Ганта")
        time.sleep(1.0)
        for e in s.mp.descendants():
            try:
                t = e.window_text().strip()
                if any(k in t for k in ("Мастер", "Стили текста", "Масштаб", "Формат отрезка")):
                    say(e.element_info.control_type, repr(t))
            except Exception:
                pass
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
