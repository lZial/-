"""Пересъёмка окна «Задание базового плана»."""
import ctypes
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import (Shot, capture, pid_of, rect, say, windows)

OUT = paths.SHOTS
user32 = ctypes.windll.user32


def wait_titled(s, title, timeout=25):
    t0 = time.time()
    while time.time() - t0 < timeout:
        for h, cls, t in windows():
            if pid_of(h) == s.pid and t.strip() == title:
                return h, t
        time.sleep(0.2)
    return None, None


def shot_onscreen(h, name, delay=2.2):
    l, t, r, b = rect(h)
    w, hh = r - l, b - t
    user32.SetWindowPos(h, 1, 0, 0, w, hh, 0x0010)
    time.sleep(delay)
    size = capture(h, os.path.join(OUT, name + ".png"))
    user32.SetWindowPos(h, 0, -4000, -4000, w, hh, 0x0004)
    time.sleep(0.4)
    return size


def main():
    s = Shot()
    s.show = lambda: None
    try:
        s.menu("Сервис", "Отслеживание", "Задать базовый план...")
        h, t = wait_titled(s, "Задание базового плана")
        if not h:
            say("FAIL: нет окна задания базового плана")
            return
        d = s.dlg_ui(h)
        for e in d.descendants(control_type="ComboBox"):
            try:
                say("combo:", repr(e.window_text()), "->", e.selected_text())
            except Exception:
                pass
        say("shot", shot_onscreen(h, "10_задать_базовый_план"))
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
