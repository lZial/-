"""Диагностика диалога «Изменение рабочего времени»: все дочерние окна."""
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
CB_GETCOUNT, CB_GETLBTEXT, CB_GETLBTEXTLEN, CB_GETCURSEL, CB_GETDROPPEDSTATE = (
    0x0146, 0x0148, 0x0149, 0x0147, 0x0157)


def close_stray(s):
    for h, cls, title in windows():
        if cls == MAIN_CLASS or pid_of(h) != s.pid:
            continue
        try:
            user32.PostMessageW(h, 0x0010, 0, 0)
        except Exception:
            pass
    time.sleep(0.6)


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
        s.app.FileOpen(paths.EXP_MPP)
        time.sleep(4)
        close_stray(s)
        s.app.ViewApply("Лист ресурсов")
        time.sleep(1.5)
        s.menu("Сервис", "Изменить рабочее время...")
        h, title = s.wait_dialog(20)
        say("диалог:", title, h)

        def cb(c, l):
            cls = ctypes.create_unicode_buffer(128)
            user32.GetClassNameW(c, cls, 128)
            t = ctypes.create_unicode_buffer(256)
            user32.GetWindowTextW(c, t, 256)
            r = wintypes.RECT()
            user32.GetWindowRect(c, ctypes.byref(r))
            par = user32.GetParent(c)
            extra = ""
            if cls.value == "ComboBox":
                cur = user32.SendMessageW(c, CB_GETCURSEL, 0, 0)
                its = items(c)
                extra = " cur=%s/%r dropped=%s n=%s" % (
                    cur, its[cur] if 0 <= cur < len(its) else "?",
                    user32.SendMessageW(c, CB_GETDROPPEDSTATE, 0, 0), len(its))
            say("  %s %-32s id=%-5s vis=%s parent=%s rect=%s text=%r%s" % (
                c, cls.value, user32.GetDlgCtrlID(c),
                bool(user32.IsWindowVisible(c)), par,
                (r.left, r.top, r.right, r.bottom), t.value, extra))
            return True

        user32.EnumChildWindows(h, EnumChildProc(cb), 0)
        say("shot", capture(h, os.path.join(OUT, "dlg38_diag.png")))
        s.dlg_button(h, "Отмена")
    finally:
        close_stray(s)
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
