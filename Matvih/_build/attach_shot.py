"""Снимок уже открытого окна по HWND + закрытие по «Отмена»."""
import ctypes
import os
import sys
import time

from pywinauto import Desktop

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import capture, rect, say

HWND = int(sys.argv[1])
NAME = sys.argv[2]
user32 = ctypes.windll.user32


def main():
    dlg = Desktop(backend="uia").window(handle=HWND)
    say("окно:", dlg.window_text(), dlg.class_name())
    l, t, r, b = rect(HWND)
    w, hh = r - l, b - t
    user32.SetWindowPos(HWND, 1, 0, 0, w, hh, 0x0010)
    time.sleep(2.2)
    say("shot", capture(HWND, os.path.join(paths.SHOTS, NAME + ".png")))
    user32.SetWindowPos(HWND, 0, -4000, -4000, w, hh, 0x0004)
    for btn in dlg.descendants(control_type="Button"):
        if btn.window_text().strip() == "Отмена":
            btn.invoke()
            say("закрыто")
            break


if __name__ == "__main__":
    main()
