"""Снимок 26: диаграмма Ганта всего проекта (все задачи).

Окно вне экрана. Снимок делается в два шага: сначала окно получает широкий
размер, затем применяются представление и масштаб «весь проект».
Пустая панель «Шкала времени» при снимке отсекается, поэтому кадр
собирается из двух частей: шапка окна с лентой и область диаграммы.
"""
import os
import sys
import time

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, capture, say

user32 = __import__("ctypes").windll.user32


def stitch(src, dst, top_h=262, skip_to=394):
    img = Image.open(src)
    w, h = img.size
    head = img.crop((0, 0, w, top_h))
    body = img.crop((0, skip_to, w, h - 42))     # без строки состояния
    out = Image.new("RGB", (w, head.height + body.height), (255, 255, 255))
    out.paste(head, (0, 0))
    out.paste(body, (0, head.height))
    out.save(dst)
    say("сшито:", dst, out.size)


def main():
    s = Shot()
    try:
        user32.SetWindowPos(s.hwnd, 0, -4000, -4000, 1500, 1000, 0x0040)
        time.sleep(1.5)
        s.app.ViewApply("Диаграмма Ганта")
        time.sleep(2.0)
        try:
            s.app.FilterApply("Суммарные задачи", False)
            say("фильтр: Суммарные задачи")
        except Exception as e:
            say("фильтр:", str(e)[:70])
        time.sleep(1.0)
        try:
            s.app.SelectTaskField(1, "Name")
        except Exception:
            pass
        try:
            s.app.ZoomTimescale(Entire=True)
            say("масштаб: весь проект")
        except Exception as e:
            say("ZoomTimescale:", str(e)[:90])
        time.sleep(2.5)
        s.app.ViewApply("Диаграмма Ганта")
        time.sleep(2.0)
        try:
            s.app.ZoomTimescale(Entire=True)
        except Exception:
            pass
        time.sleep(2.0)
        raw = os.path.join(paths.SHOTS, "_gantt_raw.png")
        say("OK 26 raw", capture(s.hwnd, raw))
        stitch(raw, os.path.join(paths.SHOTS, "26_диаграмма_ганта.png"))
    finally:
        s.close_all()
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
