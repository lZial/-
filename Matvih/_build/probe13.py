"""Шаг 2 мастера диаграмм Ганта: дамп элементов."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, capture, pid_of, say, windows

OUT = paths.SHOTS


def wait_titled(s, title, timeout=25):
    t0 = time.time()
    while time.time() - t0 < timeout:
        for h, cls, t in windows():
            if pid_of(h) == s.pid and t.strip() == title:
                return h, t
        time.sleep(0.2)
    return None, None


def invoke_menu_item(s, text):
    for e in s.mp.descendants(control_type="MenuItem"):
        try:
            if e.window_text().strip() == text:
                e.invoke()
                return True
        except Exception:
            continue
    return False


def main():
    s = Shot()
    s.show = lambda: None
    try:
        s.app.ViewApply("Диаграмма Ганта")
        time.sleep(1.0)
        s.ribbon_tab("Формат диаграммы Ганта")
        time.sleep(1.0)
        invoke_menu_item(s, "Мастер диаграмм Ганта...")
        h, t = wait_titled(s, "Мастер диаграмм Ганта")
        say("wizard:", h)
        d = s.dlg_ui(h)
        for b in d.descendants(control_type="Button"):
            if b.window_text().strip().startswith("Далее"):
                b.invoke()
                say("Далее")
                break
        time.sleep(2.0)
        for e in d.descendants():
            try:
                t2 = e.window_text().strip()
                ct = e.element_info.control_type
                if t2 and ct not in ("Text",):
                    say("%-14s %r" % (ct, t2[:70]))
            except Exception:
                pass
        say("shot", capture(h, os.path.join(OUT, "_probe13.png")))
        for b in d.descendants(control_type="Button"):
            if b.window_text().strip() == "Отмена":
                b.invoke()
                break
    finally:
        time.sleep(1.0)
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
