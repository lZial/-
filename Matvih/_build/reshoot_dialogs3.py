"""Пересъёмка 13, 15, 22 с показом диалога на экране (иначе PrintWindow отдаёт
устаревшую картинку)."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import (Shot, capture, pid_of, say, windows)

OUT = paths.SHOTS


def wait_titled(s, title, timeout=25):
    t0 = time.time()
    while time.time() - t0 < timeout:
        for h, cls, t in windows():
            if pid_of(h) == s.pid and t.strip() == title:
                return h, t
        time.sleep(0.2)
    return None, None


def shot_onscreen(s, h, name, delay=2.2):
    import ctypes
    user32 = ctypes.windll.user32
    l, t, r, b = 0, 0, 0, 0
    from reshoot_fixed import rect
    l, t, r, b = rect(h)
    w, hh = r - l, b - t
    user32.SetWindowPos(h, 1, 0, 0, w, hh, 0x0010)  # HWND_BOTTOM, NOACTIVATE
    time.sleep(delay)
    size = capture(h, os.path.join(OUT, name + ".png"))
    user32.SetWindowPos(h, 0, -4000, -4000, w, hh, 0x0004)
    time.sleep(0.4)
    return size


def invoke_menu_item(s, text):
    for e in s.mp.descendants(control_type="MenuItem"):
        try:
            if e.window_text().strip() == text:
                e.invoke()
                return True
        except Exception:
            continue
    return False


def close_dialog(s, h):
    try:
        s.dlg_button(h, "Отмена")
    except Exception as e:
        say("  cancel:", str(e)[:90])
    time.sleep(1.2)


def main():
    s = Shot()
    s.show = lambda: None
    try:
        s.app.ViewApply("Диаграмма Ганта")
        time.sleep(1.0)
        s.ribbon_tab("Формат диаграммы Ганта")
        time.sleep(1.0)

        # ---------------- 13
        say("[13]")
        invoke_menu_item(s, "Мастер диаграмм Ганта...")
        h, t = wait_titled(s, "Мастер диаграмм Ганта")
        if h:
            d = s.dlg_ui(h)
            for e in d.descendants(control_type="RadioButton"):
                say("  радио:", repr(e.window_text()), e.is_selected())
            for e in d.descendants(control_type="RadioButton"):
                if "Критический" in e.window_text():
                    e.select()
                    say("  выбрано:", e.window_text())
                    break
            time.sleep(1.0)
            say("  shot", shot_onscreen(s, h, "13_мастер_диаграмм_ганта"))
            close_dialog(s, h)
        else:
            say("  FAIL: нет окна мастера")

        # ---------------- 15
        say("[15]")
        s.app.SelectTaskField(10, "Name", False)
        time.sleep(0.8)
        invoke_menu_item(s, "Стили текста...")
        h, t = wait_titled(s, "Стили текста")
        if h:
            combo = None
            for e in s.dlg_ui(h).descendants(control_type="ComboBox"):
                if "элемент" in e.window_text():
                    combo = e
                    break
            if combo is not None:
                say("  было:", combo.selected_text())
                combo.expand()
                time.sleep(0.8)
                for it in combo.descendants(control_type="ListItem"):
                    if it.window_text().strip() == "Задачи-вехи":
                        it.select()
                        say("  выбрано:", it.window_text())
                        break
                combo.collapse()
                time.sleep(1.0)
                say("  стало:", combo.selected_text())
            say("  shot", shot_onscreen(s, h, "15_стили_текста"))
            close_dialog(s, h)
        else:
            say("  FAIL: нет окна стилей")

        # ---------------- 22
        say("[22]")
        s.app.SelectTaskField(29, "Name", False)
        time.sleep(0.8)
        invoke_menu_item(s, "Формат отрезка...")
        h, t = wait_titled(s, "Формат отрезка")
        if h:
            say("  shot", shot_onscreen(s, h, "22_формат_отрезка"))
            close_dialog(s, h)
        else:
            say("  FAIL: нет окна формата отрезка")
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
