"""Пересъёмка окна «Параметры страницы»."""
import ctypes
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import (Shot, capture, pid_of, rect, say, windows)

OUT = paths.SHOTS
user32 = ctypes.windll.user32


def wait_dialog_like(s, part, timeout=25):
    t0 = time.time()
    while time.time() - t0 < timeout:
        for h, cls, t in windows():
            if pid_of(h) == s.pid and part in t:
                return h, t
        time.sleep(0.2)
    return None, None


def main():
    s = Shot()
    s.show = lambda: None
    try:
        for path in (("Файл", "Параметры страницы..."),
                     ("Файл", "Печать", "Параметры страницы...")):
            try:
                s.menu(*path)
            except Exception as e:
                say("меню:", str(e)[:80])
            h, t = wait_dialog_like(s, "Параметры страницы", 8)
            if h:
                say("диалог:", t, h)
                break
        if not h:
            say("FAIL: окно не найдено")
            return
        time.sleep(1.0)
        l, tt, r, b = rect(h)
        w, hh = r - l, b - tt
        user32.SetWindowPos(h, 1, 0, 0, w, hh, 0x0010)
        time.sleep(2.2)
        say("shot", capture(h, os.path.join(OUT, "12_параметры_страницы.png")))
        user32.SetWindowPos(h, 0, -4000, -4000, w, hh, 0x0004)
        d = s.dlg_ui(h)
        for btn in d.descendants(control_type="Button"):
            if btn.window_text().strip() == "Отмена":
                btn.invoke()
                break
    finally:
        time.sleep(1.0)
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
