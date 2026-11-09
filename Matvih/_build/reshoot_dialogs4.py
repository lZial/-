"""Финальная пересъёмка диалогов 13, 16, 22."""
import ctypes
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import (Shot, capture, pid_of, rect, say, windows)

OUT = paths.SHOTS
user32 = ctypes.windll.user32


def wait_titled(s, title, timeout=25):
    t0 = time.time()
    while time.time() - t0 < timeout:
        for h, cls, t in windows():
            if pid_of(h) == s.pid and t.strip() == title:
                return h, t
        time.sleep(0.2)
    return None, None


def shot_onscreen(s, h, name, delay=2.2):
    l, t, r, b = rect(h)
    w, hh = r - l, b - t
    user32.SetWindowPos(h, 1, 0, 0, w, hh, 0x0010)
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


def dlg_button(d, text):
    for b in d.descendants(control_type="Button"):
        try:
            if b.window_text().strip() == text:
                b.invoke()
                return True
        except Exception:
            pass
    return False


def main():
    s = Shot()
    s.show = lambda: None
    try:
        s.app.ViewApply("Диаграмма Ганта")
        time.sleep(1.0)

        # ---------------------------------------------------------- 16
        say("[16]")
        s.menu("Вид", "Масштаб...")
        h, t = wait_titled(s, "Масштаб")
        if h:
            d = s.dlg_ui(h)
            for e in d.descendants(control_type="RadioButton"):
                if e.window_text().strip() == "1 месяц":
                    e.select()
                    break
            time.sleep(1.0)
            say("  shot", shot_onscreen(s, h, "16_масштаб"))
            dlg_button(d, "Отмена")
            time.sleep(1.5)
        else:
            say("  FAIL: нет окна масштаба")

        # ---------------------------------------------------------- 13
        say("[13]")
        s.ribbon_tab("Формат диаграммы Ганта")
        time.sleep(1.0)
        if not invoke_menu_item(s, "Мастер диаграмм Ганта..."):
            say("  FAIL: пункт меню не найден")
        h, t = wait_titled(s, "Мастер диаграмм Ганта")
        if h:
            d = s.dlg_ui(h)
            dlg_button(d, "Далее >") or dlg_button(d, "Далее")
            time.sleep(2.0)
            picked = False
            for e in d.descendants(control_type="RadioButton"):
                if e.window_text().strip() == "Критический путь":
                    e.select()
                    picked = True
                    break
            say("  критический путь:", picked)
            time.sleep(1.0)
            say("  shot", shot_onscreen(s, h, "13_мастер_диаграмм_ганта"))
            dlg_button(d, "Отмена")
            time.sleep(1.5)
        else:
            say("  FAIL: нет мастера")

        # ---------------------------------------------------------- 22
        say("[22]")
        s.app.SelectTaskField(29, "Name", False)
        time.sleep(1.0)
        s.ribbon_tab("Формат диаграммы Ганта")
        time.sleep(1.0)
        if not invoke_menu_item(s, "Формат отрезка..."):
            say("  FAIL: пункт «Формат отрезка» не найден")
        h, t = wait_titled(s, "Формат отрезка", 15)
        if h:
            say("  shot", shot_onscreen(s, h, "22_формат_отрезка"))
            dlg_button(s.dlg_ui(h), "Отмена")
            time.sleep(1.5)
        else:
            say("  FAIL: нет окна формата отрезка")
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
