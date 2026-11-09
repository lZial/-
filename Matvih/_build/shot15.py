"""Выбор элемента «Задачи-вехи» и снимок диалога «Стили текста»."""
import ctypes
import os
import sys
import time

from pywinauto import Desktop

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import capture, rect, say

HWND = int(sys.argv[1]) if len(sys.argv) > 1 else 3802460
user32 = ctypes.windll.user32


def main():
    dlg = Desktop(backend="uia").window(handle=HWND)
    combo = None
    for e in dlg.descendants(control_type="ComboBox"):
        if e.window_text().startswith("Изменяемый элемент"):
            combo = e
            break
    if combo is None:
        say("комбо не найдено")
        return
    say("было:", combo.selected_text())
    combo.expand()
    time.sleep(0.8)
    for it in combo.descendants(control_type="ListItem"):
        if it.window_text().strip() == "Задачи-вехи":
            it.select()
            say("выбрано:", it.window_text())
            break
    try:
        combo.collapse()
    except Exception:
        pass
    time.sleep(1.2)
    say("стало:", combo.selected_text())

    l, t, r, b = rect(HWND)
    w, hh = r - l, b - t
    user32.SetWindowPos(HWND, 1, 0, 0, w, hh, 0x0010)
    time.sleep(2.4)
    size = capture(HWND, os.path.join(paths.SHOTS, "15_стили_текста.png"))
    user32.SetWindowPos(HWND, 0, -4000, -4000, w, hh, 0x0004)
    say("shot", size)

    for btn in dlg.descendants(control_type="Button"):
        if btn.window_text().strip() == "Отмена":
            btn.invoke()
            say("закрыто")
            break


if __name__ == "__main__":
    main()
