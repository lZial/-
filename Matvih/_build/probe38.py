"""Проба выбора календаря в диалоге «Изменение рабочего времени»."""
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
CB_SETCURSEL, WM_COMMAND, CBN_SELCHANGE = 0x014E, 0x0111, 1
WM_KEYDOWN, WM_KEYUP, VK_DOWN, VK_UP = 0x0100, 0x0101, 0x28, 0x26


def close_stray(s):
    for h, cls, title in windows():
        if cls == MAIN_CLASS or pid_of(h) != s.pid:
            continue
        try:
            user32.PostMessageW(h, 0x0010, 0, 0)
        except Exception:
            pass
    time.sleep(0.6)


def children(h):
    res = []

    def cb(c, l):
        cls = ctypes.create_unicode_buffer(128)
        user32.GetClassNameW(c, cls, 128)
        res.append((c, cls.value, user32.GetDlgCtrlID(c)))
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
        s.menu("Сервис", "Изменить рабочее время...")
        h, title = s.wait_dialog(20)
        say("диалог:", title, h)
        combo = None
        for c, cls, cid in children(h):
            if cls == "ComboBox" and cid == 8:
                combo = c
        say("combo:", combo, "parent:", user32.GetParent(combo),
            "dialog:", h)
        its = items(combo)
        cur = user32.SendMessageW(combo, CB_GETCURSEL, 0, 0)
        say("current:", cur, its[cur] if 0 <= cur < len(its) else "?")

        # вариант 1: CB_SETCURSEL индекса календаря + уведомление родителю
        idx = its.index("Календарь МИ (апрель)")
        user32.SendMessageW(combo, CB_SETCURSEL, idx, 0)
        time.sleep(0.5)
        say("after setcursel:", user32.SendMessageW(combo, CB_GETCURSEL, 0, 0))
        user32.SendMessageW(user32.GetParent(combo), WM_COMMAND,
                            (CBN_SELCHANGE << 16) | 8, combo)
        time.sleep(2.0)
        cur = user32.SendMessageW(combo, CB_GETCURSEL, 0, 0)
        say("после notify:", cur, its[cur] if 0 <= cur < len(its) else "?")
        say("shot1", capture(h, os.path.join(OUT, "dlg38_c1.png")))

        # вариант 2: клавиши вниз к элементу ML-инженер
        target = its.index("ML-инженер")
        cur = user32.SendMessageW(combo, CB_GETCURSEL, 0, 0)
        key = VK_DOWN if target > cur else VK_UP
        for _ in range(abs(target - cur)):
            user32.SendMessageW(combo, WM_KEYDOWN, key, 0)
            user32.SendMessageW(combo, WM_KEYUP, key, 0)
            time.sleep(0.15)
        time.sleep(2.0)
        cur = user32.SendMessageW(combo, CB_GETCURSEL, 0, 0)
        say("после клавиш:", cur, its[cur] if 0 <= cur < len(its) else "?")
        say("shot2", capture(h, os.path.join(OUT, "dlg38_c2.png")))
        s.dlg_button(h, "Отмена")
    finally:
        close_stray(s)
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
