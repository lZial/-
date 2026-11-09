"""Проверка сетевого графика, календаря и графика ресурсов."""
import ctypes
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import MAIN_CLASS, Shot, capture, pid_of, say, windows

user32 = ctypes.windll.user32
OUT = os.path.join(paths.BUILD, "_probe")
os.makedirs(OUT, exist_ok=True)


def close_stray(s):
    for h, cls, title in windows():
        if cls == MAIN_CLASS or pid_of(h) != s.pid:
            continue
        try:
            user32.PostMessageW(h, 0x0010, 0, 0)
            say("   закрыто:", title)
        except Exception:
            pass
    time.sleep(0.8)


def try_view(s, key, name):
    try:
        s.app.ViewApply(name)
        time.sleep(2.0)
        try:
            s.app.FilterApply("Все задачи", False)
        except Exception:
            pass
        time.sleep(1.2)
        say(key, "->", name, capture(s.hwnd, os.path.join(OUT, key + ".png")))
        return True
    except Exception as e:
        say(key, "FAIL", str(e)[:130])
        close_stray(s)
        return False


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
        try_view(s, "network2", "Сетевой график")
        try_view(s, "calendar2", "Календарь")
        try:
            s.app.SelectResourceField(6, "Name", False)
            time.sleep(0.5)
            say("ресурс:", s.app.ActiveCell.Text)
        except Exception as e:
            say("select resource:", str(e)[:90])
        try_view(s, "graph1", "График ресурсов")
        try_view(s, "graph2", "Диаграмма использования ресурсов")
    finally:
        close_stray(s)
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
