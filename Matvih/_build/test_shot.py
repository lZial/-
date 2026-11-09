"""Тест: снимок диалога «Сведения о проекте» без показа окна."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, capture

s = Shot()
s.show = lambda: None
try:
    s.menu("Проект", "Сведения о проекте...")
    h, title = s.wait_dialog()
    print("dialog", h, title)
    if h:
        print("size", capture(h, os.path.join(paths.SHOTS, "01_сведения_о_проекте.png")))
finally:
    s.close_all()
    try:
        s.app.FileQuit()
    except Exception:
        pass
