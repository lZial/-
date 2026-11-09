"""Снимок 38: индивидуальный календарь ресурса «Мобильный разработчик».

В экспериментальной копии у ресурса изменены рабочие дни: пятницы апреля 2025
объявлены нерабочими. Диалог «Изменение рабочего времени» открывается для
календаря ресурса и переводится на апрель 2025 (PageUp).
"""
import ctypes
import os
import sys
import time
from ctypes import wintypes

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, capture, rect, say
from pywinauto.keyboard import send_keys
import win32clipboard

user32 = ctypes.windll.user32
EnumChildProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
CB_GETCOUNT, CB_GETLBTEXT, CB_GETLBTEXTLEN, CB_GETCURSEL = 0x0146, 0x0148, 0x0149, 0x0147


def place(h, x=0, y=0):
    l, t, r, b = rect(h)
    user32.SetWindowPos(h, 0, x, y, r - l, b - t, 0x0040)
    time.sleep(1.3)


def children(h):
    res = []

    def cb(c, l):
        cls = ctypes.create_unicode_buffer(128)
        user32.GetClassNameW(c, cls, 128)
        res.append((c, cls.value, user32.GetDlgCtrlID(c),
                    bool(user32.IsWindowVisible(c))))
        return True

    user32.EnumChildWindows(h, EnumChildProc(cb), 0)
    return res


def combo_items(c):
    n = user32.SendMessageW(c, CB_GETCOUNT, 0, 0)
    out = []
    for i in range(n):
        ln = user32.SendMessageW(c, CB_GETLBTEXTLEN, i, 0)
        buf = ctypes.create_unicode_buffer(max(ln, 0) + 2)
        user32.SendMessageW(c, CB_GETLBTEXT, i, ctypes.byref(buf))
        out.append(buf.value)
    return out


def click(x, y):
    user32.SetCursorPos(int(x), int(y))
    time.sleep(0.25)
    user32.mouse_event(0x0002, 0, 0, 0, 0)
    user32.mouse_event(0x0004, 0, 0, 0, 0)
    time.sleep(0.6)


def paste_text(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, text)
    win32clipboard.CloseClipboard()
    send_keys("^a")
    time.sleep(0.2)
    send_keys("^v")
    time.sleep(0.5)


def pick_calendar(h, target):
    combo = None
    for c, cls, cid, vis in children(h):
        if cls == "ComboBox" and vis and cid == 8:
            combo = c
    if combo is None:
        raise RuntimeError("список календарей не найден")
    items = combo_items(combo)
    idx = next(i for i, t in enumerate(items) if target in t)
    cur = user32.SendMessageW(combo, CB_GETCURSEL, 0, 0)
    say("календарь %d: %r (было %d)" % (idx, items[idx], cur))
    r = wintypes.RECT()
    user32.GetWindowRect(combo, ctypes.byref(r))
    click(r.right - 12, (r.top + r.bottom) // 2)
    time.sleep(1.0)
    for _ in range(idx - cur):
        send_keys("{DOWN}")
        time.sleep(0.12)
    send_keys("{ENTER}")
    time.sleep(1.5)


def name_exception(s, h):
    """Задаёт название исключения прямо в таблице (F2 — правка ячейки)."""
    place(h)
    click(250, 592)
    time.sleep(0.5)
    send_keys("{F2}")
    time.sleep(0.5)
    paste_text("Пятницы апреля 2025 г. - нерабочие дни")
    send_keys("{ENTER}")
    time.sleep(1.0)
    return True


def main():
    s = Shot()
    try:
        s.app.FileOpen(paths.EXP_MPP)
        time.sleep(5)
        s.app.ViewApply("Лист ресурсов")
        time.sleep(1.0)
        s.menu("Сервис", "Изменить рабочее время...")
        h, title = s.wait_dialog()
        say("диалог:", title, h)
        if not h:
            raise RuntimeError("диалог не открылся")
        place(h)
        pick_calendar(h, "Мобильный разработчик")
        try:
            name_exception(s, h)
        except Exception as e:
            say("   имя исключения не задано:", str(e)[:90])
        # апрель 2025: PGUP от текущего месяца шесть раз
        click(451, 415)
        time.sleep(0.4)
        for _ in range(6):
            send_keys("{PGUP}")
            time.sleep(0.35)
        time.sleep(1.0)
        try:
            name_exception(s, h)
        except Exception as e:
            say("   имя исключения не задано:", str(e)[:90])
        place(h)
        say("OK 38", capture(h, os.path.join(paths.SHOTS, "38_календарь_ресурса.png")))
        place(h, -4000, -4000)
        s.dlg_button(h, "Отмена")
    finally:
        s.close_all()
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
