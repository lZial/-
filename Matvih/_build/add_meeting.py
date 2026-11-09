"""Добавляет повторяющуюся задачу «Совещание» в конец плана."""
import os
import sys
import time

from pywinauto import Application

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot as S


def fill_dialog(hwnd):
    app = Application(backend="win32").connect(handle=hwnd)
    d = app.window(handle=hwnd)
    d.set_focus()
    time.sleep(0.5)

    name = d.child_window(class_name="JWinproj-Edit", found_index=0)
    name.set_edit_text("Совещание")
    time.sleep(0.3)

    dur = d.child_window(title_re=".*день.*", class_name="JWinproj-Edit")
    dur.set_edit_text("1 ч")
    time.sleep(0.3)

    d.child_window(title="Е&женедельно", class_name="Button").click()
    time.sleep(0.8)

    fri = d.child_window(title="пятни&цам", class_name="Button")
    if not fri.is_checked():
        fri.click()
    time.sleep(0.3)

    start = d.child_window(title_re=".*02\\.02\\.26.*", class_name="Edit")
    start.set_edit_text("06.02.26")
    start.type_keys("{TAB}")
    time.sleep(1.0)

    d.child_window(title="ОК", class_name="Button").click()
    time.sleep(4)


def main():
    s = S.Shooter()
    try:
        p = s.app.ActiveProject
        n = p.Tasks.Count
        s.app.SelectTaskField(Row=n, Column="Name", RowRelative=False)
        time.sleep(1.0)
        if not s.menu("Вставка", "Повторяющаяся задача..."):
            raise RuntimeError("меню не открыто")
        # ищем диалог
        dlg = None
        t0 = time.time()
        while time.time() - t0 < 20:
            for h, cls, title in s.proc_windows():
                if cls == "JWinproj-MLSDialog":
                    dlg = h
                    break
            if dlg:
                break
            time.sleep(0.5)
        if not dlg:
            raise RuntimeError("диалог не найден")
        time.sleep(1.0)
        fill_dialog(dlg)
        time.sleep(2)
        print("задач после вставки:", p.Tasks.Count)
        p.Save()
        print("сохранено")
    finally:
        try:
            s.app.FileQuit(0)
        except Exception:
            pass


if __name__ == "__main__":
    main()
