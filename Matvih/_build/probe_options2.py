"""Переключение раздела «Расписание» в «Параметры Project» сообщением мыши."""
import ctypes
import os
import sys
import time
from ctypes import wintypes

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, capture, rect, say

user32 = ctypes.windll.user32
WM_LBUTTONDOWN, WM_LBUTTONUP, WM_MOUSEMOVE = 0x0201, 0x0202, 0x0200
MK_LBUTTON = 0x0001
OUT = paths.SHOTS


def send_click(hwnd, x, y):
    lp = (y << 16) | (x & 0xFFFF)
    user32.PostMessageW(hwnd, WM_MOUSEMOVE, 0, lp)
    user32.PostMessageW(hwnd, WM_LBUTTONDOWN, MK_LBUTTON, lp)
    time.sleep(0.1)
    user32.PostMessageW(hwnd, WM_LBUTTONUP, 0, lp)
    time.sleep(1.2)


def main():
    s = Shot()
    s.show = lambda: None
    try:
        s.menu("Сервис", "Параметры...")
        h, title = s.wait_dialog(20)
        say("диалог:", title, h)
        d = s.dlg_ui(h)
        item = None
        for e in d.descendants(control_type="ListItem"):
            if e.window_text().strip() == "Расписание":
                item = e
                break
        say("элемент:", item)
        r = item.rectangle()
        lst = item.parent()
        lr = lst.rectangle()
        say("list rect:", lr, "item rect:", r,
            "hwnd:", lst.element_info.handle,
            "class:", lst.element_info.class_name)
        cx = (r.left + r.right) // 2 - lr.left
        cy = (r.top + r.bottom) // 2 - lr.top
        say("click in list:", cx, cy)
        send_click(lst.element_info.handle, cx, cy)
        time.sleep(1.5)
        # проверить, что открылась страница расписания
        found = False
        for e in d.descendants(control_type="Text"):
            try:
                if "расписан" in e.window_text().lower():
                    say("текст:", e.window_text())
                    found = True
            except Exception:
                pass
        say("страница расписания:", found)
        say("shot", capture(h, os.path.join(OUT, "_probe_21.png")))
        s.dlg_button(h, "Отмена")
    finally:
        s.close_all()
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
