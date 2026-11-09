"""Пересъёмка графика ресурса: перебор имён представления."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, capture, say

OUT = os.path.join(paths.BUILD, "32_new.png")
NAMES = ("Диаграмма использования ресурсов", "График ресурсов",
         "График загрузки ресурсов", "Resource Usage")


def main():
    s = Shot()
    try:
        s.app.ViewApply("Лист ресурсов")
        time.sleep(1.5)
        say("выбор ресурса:", s.select_task("Бэкенд-разработчик", 7))
        time.sleep(0.8)
        for name in NAMES:
            try:
                s.app.ViewApply(name)
                say("view ok:", name)
                time.sleep(2.5)
                say("shot:", capture(s.hwnd, OUT))
                return
            except Exception as e:
                say("view fail:", name, str(e)[:80])
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
