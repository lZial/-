# -*- coding: utf-8 -*-
"""Съёмка диалога «Изменение рабочего времени» (рис. 23) с календарём 2027."""
import ctypes
import os
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"D:\UP_MobileBank\_build")
import paths
from reshoot_fixed import Shot, capture, rect, say

user32 = ctypes.windll.user32
TMP = r"D:\UP_MobileBank\_build\_cal_shot.mpp"
OUT = os.path.join(paths.SHOTS, "04_изменить_рабочее_время.png")

s = Shot()
try:
    s.app.FileOpen(TMP)
    time.sleep(3)
    s.show()
    time.sleep(0.8)
    if not s.menu("Сервис", "Изменить рабочее время..."):
        raise RuntimeError("нет меню")
    h, title = s.wait_dialog(15)
    say("диалог:", title)
    if not h:
        raise RuntimeError("нет диалога")
    l, t, r, b = rect(h)
    user32.SetWindowPos(h, 0, 0, 0, r - l, b - t, 0x0040)
    time.sleep(2.0)
    d = s.dlg_ui(h)
    down = [e for e in d.descendants(control_type="Button")
            if e.window_text().strip() == "Прокрутить вниз"]
    for _ in range(3):
        down[0].click_input()
        time.sleep(0.9)
    # клик по 23 февраля 2027: 4-я строка, 2-й столбец сетки
    pane = None
    for e in d.descendants(control_type="Pane"):
        if e.window_text().strip() == "Календарь":
            pane = e
            break
    say("pane:", pane.rectangle() if pane else None)
    if pane:
        rc = pane.rectangle()
        # ширина сетки без вертикальной полосы прокрутки
        grid_w = rc.right - rc.left - 26
        cw = grid_w / 7.0
        # шапка с днём недели + строка чисел месяца
        header = 58
        rh = (rc.bottom - rc.top - header) / 6.0
        cx = int(rc.left + cw * 1.5)
        cy = int(rc.top + header + rh * 3.5)
        say("click at", cx, cy)
        user32.SetCursorPos(cx, cy)
        time.sleep(0.3)
        user32.mouse_event(0x0002, 0, 0, 0, 0)
        time.sleep(0.1)
        user32.mouse_event(0x0004, 0, 0, 0, 0)
        time.sleep(1.5)
    for e in d.descendants(control_type="Text"):
        t2 = e.window_text().strip()
        if "Рабочие часы" in t2 or "не является" in t2:
            say("TEXT:", t2[:120])
    time.sleep(0.5)
    l, t, r, b = rect(h)
    user32.SetWindowPos(h, 0, -4000, -4000, r - l, b - t, 0x0004)
    time.sleep(0.8)
    say("OK", capture(h, OUT))
    time.sleep(0.4)
    try:
        s.dlg_button(h, "Отмена")
    except Exception:
        pass
finally:
    try:
        s.app.FileQuit()
    except Exception:
        pass
say("done")
