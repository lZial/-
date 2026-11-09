"""Разведка классических отчетов MS Project («Отчеты...»)."""
import ctypes
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, capture, pid_of, say, windows

user32 = ctypes.windll.user32


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
        s.ribbon_tab("Проект")
        time.sleep(1.0)
        say("--- пункты с «отчет» ---")
        for e in s.mp.descendants():
            try:
                t = e.window_text().strip()
            except Exception:
                continue
            if "отч" in t.lower() or "отчёт" in t.lower():
                say(getattr(e.element_info, "control_type", "?"), "|", t)
        el = find(s.mp, "Отчеты...")
        if el is None:
            say("нет «Отчеты...»")
            return
        say("click Отчеты...")
        el.click_input()
        time.sleep(4)
        say("--- окна ---")
        for h, cls, t in windows():
            if pid_of(h) == s.pid:
                say(h, cls, repr(t))
        # снимок главного окна/диалога
        target = s.hwnd
        for h, cls, t in windows():
            if pid_of(h) == s.pid and t and "отчет" in t.lower():
                target = h
                break
        l, top, r, b = __import__("reshoot_fixed").rect(target)
        w, hh = r - l, b - top
        user32.SetWindowPos(target, 1, 0, 0, w, hh, 0x0010)
        time.sleep(2.5)
        say("shot:", capture(target, os.path.join(paths.BUILD, "_probe_reports_dialog.png")))
        user32.SetWindowPos(target, 0, -4000, -4000, w, hh, 0x0004)
    finally:
        time.sleep(1.0)
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
