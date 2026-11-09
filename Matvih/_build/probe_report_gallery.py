"""Разведка подменю галереи «Панели мониторинга»."""
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
        s.ribbon_tab("Отчет")
        time.sleep(1.0)
        item = find(s.mp, "Панели мониторинга")
        if item is None:
            say("нет Панели мониторинга")
            return
        say("click:", item.element_info.control_type)
        item.click_input()
        time.sleep(2.0)
        say("--- windows ---")
        for h, cls, t in windows():
            if pid_of(h) == s.pid:
                say(h, cls, repr(t))
        say("--- named items ---")
        seen = set()
        for e in s.mp.descendants():
            try:
                t = e.window_text().strip()
            except Exception:
                continue
            if not t or t in seen:
                continue
            seen.add(t)
            if any(k in t.lower() for k in
                   ("проект", "стоимост", "ресурс", "ход", "обзор",
                    "выполн", "бюджет", "трудозатрат")):
                ct = getattr(e.element_info, "control_type", "?")
                say(ct, "|", t)
        say("shot:", capture(s.hwnd, os.path.join(paths.BUILD, "_probe_gallery.png")))
        # закрыть галерею
        try:
            item.click_input()
        except Exception:
            pass
    finally:
        time.sleep(1.0)
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
