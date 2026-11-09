"""Снимок визуального отчета MS Project.

Запуск: python shoot_report.py "Панели мониторинга" "Обзор проекта" 43_отчет_обзор_проекта
"""
import ctypes
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, capture, pid_of, rect, say, windows

user32 = ctypes.windll.user32


def find(root, name, ctype=None):
    for e in root.descendants():
        try:
            if e.window_text().strip() != name:
                continue
            if ctype and getattr(e.element_info, "control_type", "") != ctype:
                continue
            return e
        except Exception:
            pass
    return None


def click_button(s, name, bottom=False):
    items = []
    for e in s.mp.descendants():
        try:
            if (getattr(e.element_info, "control_type", "") == "Button"
                    and e.window_text().strip() == name):
                items.append(e)
        except Exception:
            pass
    if not items:
        return False
    items.sort(key=lambda e: e.rectangle().top, reverse=bottom)
    try:
        items[0].click_input()
        return True
    except Exception as ex:
        say("click %s err: %s" % (name, str(ex)[:70]))
        return False


def main():
    gallery = sys.argv[1]
    template = sys.argv[2]
    outname = sys.argv[3]
    zoom = int(sys.argv[4]) if len(sys.argv) > 4 else 75
    s = Shot()
    try:
        # скрываем временную шкалу, если это возможно
        try:
            s.app.TimelineShow = False
        except Exception as e:
            say("TimelineShow:", str(e)[:70])
        s.show()
        s.ribbon_tab("Отчет")
        time.sleep(1.0)
        g = find(s.mp, gallery, "MenuItem")
        if g is None:
            say("НЕТ галереи:", gallery)
            return
        g.click_input()
        time.sleep(1.5)
        t = find(s.mp, template, "ListItem")
        if t is None:
            say("НЕТ шаблона:", template)
            return
        say("открываю:", gallery, "->", template)
        t.click_input()
        time.sleep(14)
        # сворачиваем ленту и уменьшаем масштаб отчета, чтобы он влез по ширине
        click_button(s, "Свернуть ленту")
        time.sleep(1.0)
        try:
            s.app.ZoomReport(zoom)
            say("ZoomReport:", zoom)
        except Exception as e:
            say("ZoomReport err:", str(e)[:80])
        time.sleep(1.5)
        l, top, r, b = rect(s.hwnd)
        user32.SetWindowPos(s.hwnd, 1, 0, 0, r - l, b - top, 0x0010)
        time.sleep(3.5)
        say("shot:", capture(s.hwnd, os.path.join(paths.SHOTS, outname + ".png")))
        user32.SetWindowPos(s.hwnd, 0, -4000, -4000, r - l, b - top, 0x0004)
        time.sleep(0.5)
    finally:
        try:
            s.app.ActiveProject.Saved = True
        except Exception:
            pass
        time.sleep(1.0)
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
