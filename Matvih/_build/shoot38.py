"""Снимок 38: индивидуальный календарь ресурса «ML-инженер» (апрель 2026).

В экспериментальной копии ресурсу назначен календарь «Календарь МИ (апрель)»,
в котором изменены рабочие часы апреля. Диалог «Изменение рабочего времени»
переводится на апрель 2026, выбирается пятница 3 апреля — видно, что день
нерабочий. Окно диалога на время снимка опускается в низ z-порядка, чтобы
элементы перерисовались, и возвращается за пределы экрана.
"""
import ctypes
import os
import sys
import time
from ctypes import wintypes

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import MAIN_CLASS, Shot, capture, pid_of, say, windows

user32 = ctypes.windll.user32
OUT = paths.SHOTS
EnumChildProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
CB_GETCOUNT, CB_GETLBTEXT, CB_GETLBTEXTLEN, CB_GETCURSEL = 0x0146, 0x0148, 0x0149, 0x0147
WM_KEYDOWN, WM_KEYUP, WM_LBUTTONDOWN, WM_LBUTTONUP, WM_MOUSEMOVE = (
    0x0100, 0x0101, 0x0201, 0x0202, 0x0200)
WM_MOUSEWHEEL = 0x020A
VK_F4, VK_DOWN, VK_UP, VK_RETURN = 0x73, 0x28, 0x26, 0x0D
MK_LBUTTON = 0x0001
HWND_BOTTOM = 1
SWP_NOSIZE, SWP_NOACTIVATE = 0x0001, 0x0010


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
    user32.PostMessageW(hwnd, WM_MOUSEMOVE, 0, lp)
    user32.PostMessageW(hwnd, WM_LBUTTONDOWN, MK_LBUTTON, lp)
    time.sleep(0.08)
    user32.PostMessageW(hwnd, WM_LBUTTONUP, 0, lp)
    time.sleep(0.8)


def static_text(h, cid):
    for c, cls, i, txt in kids(h):
        if i == cid:
            return txt
    return ""


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
        if not h:
            raise RuntimeError("диалог не открылся")

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
        say("календарь:", items(combo)[user32.SendMessageW(combo, CB_GETCURSEL, 0, 0)])
        say("базовый:", static_text(h, 6))

        # ноябрь 2026 -> апрель 2026: семь шагов назад колесом
        for _ in range(7):
            user32.SendMessageW(month, WM_MOUSEWHEEL, (120 & 0xFFFF) << 16,
                                (100 << 16) | 100)
            time.sleep(0.45)
        time.sleep(0.8)

        # пятница 3 апреля 2026
        click(month, 161, 61)
        time.sleep(0.8)
        say("часы:", static_text(h, 23))
        say("основа:", static_text(h, 26))

        # кратковременно на экран (в низ z-порядка), чтобы перерисовать
        r = wintypes.RECT()
        user32.GetWindowRect(h, ctypes.byref(r))
        w, hh = r.right - r.left, r.bottom - r.top
        user32.SetWindowPos(h, HWND_BOTTOM, 0, 0, w, hh, SWP_NOACTIVATE)
        time.sleep(2.0)
        p = os.path.join(OUT, "38_календарь_ресурса.png")
        say("снимок:", capture(h, p))
        user32.SetWindowPos(h, 0, -4000, -4000, w, hh, 0x0040)
        time.sleep(0.5)
        s.dlg_button(h, "Отмена")
    finally:
        close_stray(s)
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
