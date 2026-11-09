"""Пересъёмка представления «Лист ресурсов» на исправленном файле."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, capture, say

OUT = os.path.join(paths.BUILD, "30_new.png")


def main():
    s = Shot()
    try:
        s.ribbon_tab("Вид")
        time.sleep(0.8)
        ok = s.ribbon_button("Лист ресурсов")
        say("Лист ресурсов:", ok)
        time.sleep(2.0)
        # сворачиваем ленту, чтобы таблица занимала больше места
        for b in s.mp.descendants(control_type="Button"):
            try:
                if "Свернуть ленту" in b.window_text():
                    b.invoke()
                    time.sleep(1.0)
                    break
            except Exception:
                pass
        time.sleep(1.5)
        say("shot:", capture(s.hwnd, OUT))
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
