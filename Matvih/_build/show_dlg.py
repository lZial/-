"""Просмотр диалогов «Microsoft Project» и «Стили текста» по HWND."""
import sys

from pywinauto import Desktop

sys.stdout.reconfigure(encoding="utf-8")

for hwnd in (2556646, 3802460):
    dlg = Desktop(backend="uia").window(handle=hwnd)
    print("=" * 60)
    print(hwnd, dlg.class_name(), repr(dlg.window_text()))
    for e in dlg.descendants():
        try:
            t = e.window_text().strip()
            ct = e.element_info.control_type
            if t and ct in ("Text", "Button", "ComboBox", "RadioButton", "CheckBox"):
                print("  %-12s %r" % (ct, t[:80]))
        except Exception:
            pass
