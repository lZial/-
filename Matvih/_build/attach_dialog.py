"""Подключение к диалогу по HWND."""
import os
import sys
import time

from pywinauto import Desktop

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import capture, say

OUT = paths.SHOTS
HWND = int(sys.argv[1]) if len(sys.argv) > 1 else 3343252


def main():
    dlg = Desktop(backend="uia").window(handle=HWND)
    say("окно:", dlg.window_text(), dlg.class_name())
    for e in dlg.descendants():
        try:
            ct = e.element_info.control_type
            t = e.window_text().strip()
            if ct in ("ComboBox", "Button", "CheckBox", "List"):
                say("%-12s %r" % (ct, t[:60]))
        except Exception:
            pass
    combo = None
    for e in dlg.descendants(control_type="ComboBox"):
        if "элемент" in e.window_text():
            combo = e
            break
    if combo is not None:
        say("комбо:", repr(combo.window_text()), "->", combo.selected_text())
        try:
            combo.expand()
            time.sleep(0.8)
            for it in combo.descendants(control_type="ListItem"):
                say("    пункт:", repr(it.window_text()))
                if it.window_text().strip() == "Веха":
                    it.select()
            combo.collapse()
        except Exception as exc:
            say("combo:", str(exc)[:120])
        time.sleep(1.0)
        say("стало:", combo.selected_text())
    say("shot", capture(dlg.handle, os.path.join(OUT, "15_стили_текста.png")))
    for b in dlg.descendants(control_type="Button"):
        if b.window_text().strip() == "Отмена":
            b.invoke()
            say("закрыто")
            break


if __name__ == "__main__":
    main()
