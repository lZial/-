"""Проверка применения представлений без показа окна (устойчивый вариант)."""
import ctypes
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import MAIN_CLASS, Shot, capture, move_off, pid_of, say, windows

user32 = ctypes.windll.user32
OUT = os.path.join(paths.BUILD, "_probe")
os.makedirs(OUT, exist_ok=True)

VIEWS = [
    ("gantt", "Диаграмма Ганта"),
    ("usage_tasks", "Использование задач"),
    ("network", "Сетевой график"),
    ("calendar", "Календарь"),
    ("sheet_res", "Лист ресурсов"),
    ("usage_res", "Использование ресурсов"),
    ("graph_res", "График ресурса"),
]


def close_stray(s, skip_title=""):
    closed = []
    for h, cls, title in windows():
        if cls == MAIN_CLASS or pid_of(h) != s.pid:
            continue
        if skip_title and skip_title in title:
            continue
        try:
            user32.PostMessageW(h, 0x0010, 0, 0)
            closed.append(title)
        except Exception:
            pass
    if closed:
        say("   закрыты окна:", closed)
        time.sleep(1.0)


def main():
    s = Shot()
    s.show = lambda: None
    try:
        for _ in range(40):
            if s.wait_ready(3):
                break
            close_stray(s)
        close_stray(s)
        user32.SetWindowPos(s.hwnd, 0, -4000, -4000, 1500, 1000, 0x0040)
        time.sleep(1.2)
        for key, name in VIEWS:
            try:
                s.app.ViewApply(name)
                time.sleep(2.0)
                try:
                    s.app.ZoomTimescale(Entire=True)
                except Exception:
                    pass
                time.sleep(1.0)
                p = os.path.join(OUT, key + ".png")
                say(key, "->", name, capture(s.hwnd, p))
            except Exception as e:
                say(key, "FAIL", str(e)[:120])
                close_stray(s)
    finally:
        close_stray(s)
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
