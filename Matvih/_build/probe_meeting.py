"""Открывает диалог повторяющейся задачи и печатает дерево элементов."""
import os
import sys
import time

import win32com.client as w
from pywinauto import Desktop

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths

user32 = __import__("ctypes").windll.user32


def dump(win, depth=0, out=None):
    try:
        info = win.element_info
        text = info.name or ""
        ctype = info.control_type
        auto = info.automation_id
        rect = win.rectangle()
        out.append("%s%s | %r | id=%s | (%d,%d,%d,%d)" % (
            "  " * depth, ctype, text[:80], auto,
            rect.left, rect.top, rect.right, rect.bottom))
    except Exception as e:
        out.append("%sERR %s" % ("  " * depth, str(e)[:60]))
        return
    try:
        for ch in win.children():
            dump(ch, depth + 1, out)
    except Exception:
        pass


def main():
    app = w.Dispatch("MSProject.Application")
    app.Visible = True
    app.DisplayAlerts = 0
    app.FileOpen(paths.MPP)
    time.sleep(3)
    app.RecurringTaskInsert()
    time.sleep(3)
    out = []
    dlg = None
    for win in Desktop(backend="uia").windows():
        try:
            cls = win.class_name()
            if cls == "JWinproj-WhimperMainClass":
                continue
            if win.is_visible() and win.rectangle().width() > 300:
                if "повтор" in win.window_text().lower() or "Recurring" in win.window_text():
                    dlg = win
                    break
        except Exception:
            continue
    if dlg is None:
        out.append("ДИАЛОГ НЕ НАЙДЕН")
    else:
        out.append("ДИАЛОГ: %r class=%s" % (dlg.window_text(), dlg.class_name()))
        dump(dlg, 0, out)
    with open(os.path.join(paths.BUILD, "meeting_tree.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("готово, строк:", len(out))


if __name__ == "__main__":
    main()
