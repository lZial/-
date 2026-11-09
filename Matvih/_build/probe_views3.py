"""Проверка отрисовки календаря и сетевого графика при разных способах."""
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
RDW_INVALIDATE, RDW_ERASE, RDW_ALLCHILDREN, RDW_UPDATENOW = 0x0001, 0x0004, 0x0080, 0x0100
HWND_BOTTOM = 1
SWP_NOSIZE, SWP_NOACTIVATE = 0x0001, 0x0010


def redraw(h):
    user32.RedrawWindow(h, None, None,
                        RDW_INVALIDATE | RDW_ERASE | RDW_ALLCHILDREN | RDW_UPDATENOW)
    time.sleep(1.0)


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
        r = wintypes.RECT()
        user32.GetWindowRect(s.hwnd, ctypes.byref(r))
        w, h = r.right - r.left, r.bottom - r.top
        say("размер окна:", w, h)

        for view, key in (("Календарь", "cal"), ("Сетевой график", "net")):
            try:
                s.app.ViewApply(view)
                time.sleep(2.0)
                try:
                    s.app.FilterApply("Все задачи", False)
                except Exception:
                    pass
                time.sleep(1.0)
                user32.SetWindowPos(s.hwnd, 0, -4000, -4000, w, h, 0x0040)
                time.sleep(0.5)
                redraw(s.hwnd)
                say(key + "_off", capture(s.hwnd, os.path.join(OUT, key + "_off.png")))
                # на экране, но в самом низу z-порядка
                user32.SetWindowPos(s.hwnd, HWND_BOTTOM, 0, 0, w, h,
                                    SWP_NOACTIVATE)
                time.sleep(1.5)
                redraw(s.hwnd)
                say(key + "_on", capture(s.hwnd, os.path.join(OUT, key + "_on.png")))
                user32.SetWindowPos(s.hwnd, 0, -4000, -4000, w, h, 0x0040)
                time.sleep(0.5)
            except Exception as e:
                say(key, "FAIL", str(e)[:130])
                close_stray(s)
    finally:
        close_stray(s)
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
