"""Проверка: пропадает ли звёздочка и панель вкладок после сохранения."""
import ctypes
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, capture, rect, say

user32 = ctypes.windll.user32
HWND_BOTTOM = 1
SWP_NOSIZE = 0x0001


def bottom_show(s, seconds=2.2):
    user32.SetWindowPos(s.hwnd, HWND_BOTTOM, 0, 0, 0, 0,
                        SWP_NOSIZE | 0x0040)
    time.sleep(seconds)


def bottom_hide(s):
    l, t, r, b = rect(s.hwnd)
    user32.SetWindowPos(s.hwnd, 0, -4000, -4000, r - l, b - t, 0x0040)
    time.sleep(0.8)
    s.refresh()


def main():
    s = Shot()
    s.show = lambda: None
    try:
        s.app.ViewApply("Диаграмма Ганта")
        time.sleep(1.5)
        s.app.SelectTaskField(1, "Name", False)
        s.ribbon_tab("Задача")
        time.sleep(1.0)
        try:
            s.app.FileSave()
            say("сохранено")
        except Exception as e:
            say("save:", str(e)[:90])
        time.sleep(1.0)
        bottom_show(s, 2.4)
        say("shot", capture(s.hwnd, os.path.join(paths.SHOTS, "_probe_tab33.png")))
        bottom_hide(s)
    finally:
        try:
            s.app.FileClose(0)
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
