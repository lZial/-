"""Список шаблонов в каждой галерее отчетов."""
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
        for target in ("Панели мониторинга", "Ресурсы", "Затраты",
                       "Ход выполнения", "Начало работы", "Другие"):
            item = find(s.mp, target)
            if item is None:
                say("НЕТ:", target)
                continue
            item.click_input()
            time.sleep(1.5)
            names = []
            for e in s.mp.descendants():
                try:
                    if getattr(e.element_info, "control_type", "") == "ListItem":
                        t = e.window_text().strip()
                        if t:
                            names.append(t)
                except Exception:
                    pass
            # уникальные с сохранением порядка
            uniq = []
            for n in names:
                if n not in uniq:
                    uniq.append(n)
            say("=== %s: %s" % (target, " | ".join(uniq)))
            item.click_input()
            time.sleep(0.8)
    finally:
        time.sleep(0.5)
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
