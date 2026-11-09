"""Проба: навигация по месяцам кликом по стрелке MonthBox."""
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
EnumChildProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
CB_GETCOUNT, CB_GETLBTEXT, CB_GETLBTEXTLEN, CB_GETCURSEL = 0x0146, 0x0148, 0x0149, 0x0147
WM_KEYDOWN, WM_KEYUP, WM_LBUTTONDOWN, WM_LBUTTONUP, WM_MOUSEMOVE = (
    0x0100, 0x0101, 0x0201, 0x0202, 0x0200)
VK_F4, VK_DOWN, VK_UP, VK_RETURN = 0x73, 0x28, 0x26, 0x0D
RDW_INVALIDATE, RDW_ERASE, RDW_ALLCHILDREN, RDW_UPDATENOW = 0x0001, 0x0004, 0x0080, 0x0100
MK_LBUTTON = 0x0001


def close_stray(s):
    for h, cls, title in windows():
        if cls == MAIN_CLASS or pid_of(h) != s.pid:
            continue
        try:
            user32.PostMessageW(h, 0x0010, 0, 0)
        except Exception:
            pass
    time.sleep(0.6)


def kids(h):
    res = []

    def cb(c, l):
        cls = ctypes.create_unicode_buffer(128)
        user32.GetClassNameW(c, cls, 128)
        t = ctypes.create_unicode_buffer(512)
        user32.GetWindowTextW(c, t, 512)
        res.append((c, cls.value, user32.GetDlgCtrlID(c), t.value))
        return True

    user32.EnumChildWindows(h, EnumChildProc(cb), 0)
    return res


def items(c):
    n = user32.SendMessageW(c, CB_GETCOUNT, 0, 0)
    out = []
    for i in range(n):
        ln = user32.SendMessageW(c, CB_GETLBTEXTLEN, i, 0)
        buf = ctypes.create_unicode_buffer(max(ln, 0) + 2)
        user32.SendMessageW(c, CB_GETLBTEXT, i, ctypes.byref(buf))
        out.append(buf.value)
    return out


def key(hwnd, vk):
    user32.SendMessageW(hwnd, WM_KEYDOWN, vk, 0)
    user32.SendMessageW(hwnd, WM_KEYUP, vk, 0)
    time.sleep(0.3)


def click(hwnd, x, y):
    lp = (y << 16) | (x & 0xFFFF)
    user32.SendMessageW(hwnd, WM_MOUSEMOVE, 0, lp)
    user32.SendMessageW(hwnd, WM_LBUTTONDOWN, MK_LBUTTON, lp)
    time.sleep(0.06)
    user32.SendMessageW(hwnd, WM_LBUTTONUP, 0, lp)
    time.sleep(0.5)


def hours(h):
    for c, cls, cid, txt in kids(h):
        if cid == 23:
            return txt


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
        s.app.FileOpen(paths.EXP_MPP)
        time.sleep(4)
        close_stray(s)
        s.app.ViewApply("Лист ресурсов")
        time.sleep(1.5)
        s.menu("Сервис", "Изменить рабочее время...")
        h, title = s.wait_dialog(20)
        say("диалог:", title, h)

        combo = month = None
        for c, cls, cid, txt in kids(h):
            if cls == "ComboBox" and cid == 8:
                combo = c
            elif cls == "JWinproj-WhimperMonthBox2":
                month = c
        its = items(combo)
        target = its.index("ML-инженер")
        key(combo, VK_F4)
        cur = user32.SendMessageW(combo, CB_GETCURSEL, 0, 0)
        step = VK_DOWN if target > cur else VK_UP
        for _ in range(abs(target - cur)):
            key(combo, step)
        key(combo, VK_RETURN)
        time.sleep(1.5)
        user32.RedrawWindow(combo, None, None,
                            RDW_INVALIDATE | RDW_ERASE | RDW_UPDATENOW)
        user32.UpdateWindow(combo)
        time.sleep(0.8)
        say("hours:", hours(h))
        say("shot0", capture(h, os.path.join(OUT, "dlg38d_0.png")))

        # клик по верхней стрелке MonthBox (примерно 240, 14)
        for i in range(7):
            click(month, 243, 16)
            user32.RedrawWindow(month, None, None, RDW_INVALIDATE | RDW_UPDATENOW)
        time.sleep(1.0)
        say("hours после кликов:", hours(h))
        say("shot1", capture(h, os.path.join(OUT, "dlg38d_1.png")))

        s.dlg_button(h, "Отмена")
    finally:
        close_stray(s)
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
