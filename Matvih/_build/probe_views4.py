"""Проверка графика ресурсов для ML-инженера."""
import ctypes
import os
import sys
import time
from ctypes import wintypes

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import MAIN_CLASS, Shot, capture, pid_of, say, windows

user32 = ctypes.windll.user32
OUT = os.path.join(paths.BUILD, "_probe")
os.makedirs(OUT, exist_ok=True)
HWND_BOTTOM = 1
SWP_NOACTIVATE = 0x0010


def close_stray(s):
    for h, cls, title in windows():
        if cls == MAIN_CLASS or pid_of(h) != s.pid:
            continue
        try:
            user32.PostMessageW(h, 0x0010, 0, 0)
        except Exception:
            pass
    time.sleep(0.6)


def main():
    s = Shot()
    s.show = lambda: None
    try:
        for _ in range(40):
            if s.wait_ready(3):
                break
            close_stray(s)
        close_stray(s)
        user32.SetWindowPos(s.hwnd, 0, -4000, -4000, 1500, 1000, 0x0040)
        time.sleep(1.0)
        s.app.ViewApply("Лист ресурсов")
        time.sleep(1.5)
        s.app.SelectResourceField(6, "Name", False)
        time.sleep(0.5)
        say("ресурс:", s.app.ActiveCell.Text)
        s.app.ViewApply("График ресурсов")
        time.sleep(2.0)
        try:
            s.app.ZoomTimescale(Entire=True)
            say("zoom entire ok")
        except Exception as e:
            say("zoom:", str(e)[:90])
        time.sleep(1.0)
        user32.SetWindowPos(s.hwnd, HWND_BOTTOM, 0, 0, 1500, 1000, SWP_NOACTIVATE)
        time.sleep(2.0)
        say("graph", capture(s.hwnd, os.path.join(OUT, "graph_ml.png")))
        user32.SetWindowPos(s.hwnd, 0, -4000, -4000, 1500, 1000, 0x0040)
    finally:
        close_stray(s)
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
