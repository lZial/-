"""Съёмка вкладок ленты: после переключения вкладки окно кратко
показывается внизу экрана, чтобы таблица и лента успели перерисоваться."""
import ctypes
import os
import sys
import time
from ctypes import wintypes

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, capture, rect, say

user32 = ctypes.windll.user32
OUT = paths.SHOTS
HWND_BOTTOM = 1
SWP_NOSIZE = 0x0001


def bottom_show(s, seconds=2.2):
    l, t, r, b = rect(s.hwnd)
    user32.SetWindowPos(s.hwnd, HWND_BOTTOM, 0, 0, 0, 0,
                        SWP_NOSIZE | 0x0040)
    time.sleep(seconds)


def bottom_hide(s):
    l, t, r, b = rect(s.hwnd)
    user32.SetWindowPos(s.hwnd, 0, -4000, -4000, r - l, b - t, 0x0040)
    time.sleep(0.8)
    s.refresh()


def shoot_tab(s, name, tab, save=False):
    s.app.ViewApply("Диаграмма Ганта")
    time.sleep(1.5)
    s.app.SelectTaskField(1, "Name", False)
    time.sleep(0.8)
    if save:
        try:
            s.app.FileSave()
            say("сохранено")
        except Exception as e:
            say("save:", str(e)[:90])
        time.sleep(1.0)
    s.ribbon_tab(tab)
    time.sleep(1.0)
    bottom_show(s, 2.4)
    size = capture(s.hwnd, os.path.join(OUT, name + ".png"))
    say("OK %-24s %s" % (name, size))
    bottom_hide(s)


def main():
    s = Shot()
    s.show = lambda: None
    try:
        first = True
        for name, tab in (("33_вкладка_задача", "Задача"),
                          ("34_вкладка_ресурс", "Ресурс"),
                          ("35_вкладка_проект", "Проект"),
                          ("36_вкладка_отчет", "Отчет")):
            for attempt in range(3):
                try:
                    shoot_tab(s, name, tab, save=True)
                    first = False
                    break
                except Exception as e:
                    say("retry", name, str(e)[:90])
                    time.sleep(3)
    finally:
        try:
            s.app.FileClose(0)
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
