"""Проба выбора календаря в диалоге «Изменение рабочего времени» (стратегии)."""
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
CB_SETCURSEL, CB_SHOWDROPDOWN = 0x014E, 0x014F
WM_COMMAND, WM_KEYDOWN, WM_KEYUP = 0x0111, 0x0100, 0x0101
CBN_SELCHANGE, CBN_SELENDOK = 1, 9
VK_F4, VK_DOWN, VK_UP, VK_RETURN, VK_ESCAPE = 0x73, 0x28, 0x26, 0x0D, 0x1B


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


def state(h, combo):
    cur = user32.SendMessageW(combo, CB_GETCURSEL, 0, 0)
    its = items(combo)
    base = ""
    hours = ""
    based = ""
    for c, cls, cid, txt in kids(h):
        if cid == 6 and cls == "JWinproj-Edit":
            base = txt
        elif cid == 23:
            hours = txt
        elif cid == 26:
            based = txt.replace("\n", " ")
    return "cur=%s/%r base=%r hours=%r based=%r" % (
        cur, its[cur] if 0 <= cur < len(its) else "?", base, hours, based)


def key(hwnd, vk):
    user32.SendMessageW(hwnd, WM_KEYDOWN, vk, 0)
    user32.SendMessageW(hwnd, WM_KEYUP, vk, 0)
    time.sleep(0.25)


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

        # определить окна
        combo = None
        combo_base = None
        month = None
        for c, cls, cid, txt in kids(h):
            if cls == "ComboBox" and cid == 8:
                combo = c
            elif cls == "ComboBox" and cid == 10:
                combo_base = c
            elif cls == "JWinproj-WhimperMonthBox2":
                month = c
        say("combo=%s base_combo=%s month=%s" % (combo, combo_base, month))
        say("исходно:", state(h, combo))

        its = items(combo)
        target = its.index("ML-инженер")
        say("цель ML-инженер idx=%s" % target)

        # --- стратегия B: F4, стрелки, Enter
        key(combo, VK_F4)
        say("после F4 dropped=%s" % user32.SendMessageW(combo, 0x0157, 0, 0))
        cur = user32.SendMessageW(combo, CB_GETCURSEL, 0, 0)
        step = VK_DOWN if target > cur else VK_UP
        for _ in range(abs(target - cur)):
            key(combo, step)
        key(combo, VK_RETURN)
        time.sleep(1.5)
        say("B после Enter:", state(h, combo))
        say("shotB", capture(h, os.path.join(OUT, "dlg38_B.png")))

        # --- стратегия A: CB_SETCURSEL + CBN_SELCHANGE/SELENDOK
        if "ML-инженер" not in state(h, combo):
            user32.SendMessageW(combo, CB_SETCURSEL, target, 0)
            user32.SendMessageW(h, WM_COMMAND,
                                (CBN_SELCHANGE << 16) | 8, combo)
            user32.SendMessageW(h, WM_COMMAND,
                                (CBN_SELENDOK << 16) | 8, combo)
            time.sleep(1.5)
            say("A после notify:", state(h, combo))
            say("shotA", capture(h, os.path.join(OUT, "dlg38_A.png")))

        # --- стратегия C: dropdown + стрелки + enter
        if "ML-инженер" not in state(h, combo):
            user32.SendMessageW(combo, CB_SHOWDROPDOWN, 1, 0)
            time.sleep(0.8)
            say("C dropped=%s" % user32.SendMessageW(combo, 0x0157, 0, 0))
            cur = user32.SendMessageW(combo, CB_GETCURSEL, 0, 0)
            step = VK_DOWN if target > cur else VK_UP
            for _ in range(abs(target - cur)):
                key(combo, step)
            key(combo, VK_RETURN)
            time.sleep(1.5)
            say("C после Enter:", state(h, combo))
            say("shotC", capture(h, os.path.join(OUT, "dlg38_C.png")))

        say("итог:", state(h, combo))
        s.dlg_button(h, "Отмена")
    finally:
        close_stray(s)
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
