"""Снимок 40: вкладка «Затраты» диалога «Сведения о ресурсе».

Ресурс выбирается по абсолютной строке листа ресурсов
(SelectResourceField(6, "Name", False)), диалог открывается кнопкой
«Сведения...» на вкладке ленты «Ресурс».
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, capture, rect, say

user32 = __import__("ctypes").windll.user32


def place(h, x=0, y=0):
    l, t, r, b = rect(h)
    user32.SetWindowPos(h, 0, x, y, r - l, b - t, 0x0040)
    time.sleep(1.4)


def main():
    s = Shot()
    try:
        s.app.FileOpen(paths.EXP_MPP)
        time.sleep(5)
        s.app.ViewApply("Лист ресурсов")
        time.sleep(1.2)
        s.app.SelectResourceField(6, "Name", False)
        time.sleep(0.5)
        say("ресурс:", s.app.ActiveCell.Text)
        s.show()
        say("вкладка Ресурс:", s.ribbon_tab("Ресурс"))
        ok = False
        for b in s.mp.descendants(control_type="Button"):
            try:
                if b.window_text().strip() == "Сведения...":
                    say("нажимаю «Сведения...»")
                    b.invoke()
                    ok = True
                    break
            except Exception:
                pass
        if not ok:
            raise RuntimeError("кнопка «Сведения...» не найдена")
        h, title = s.wait_dialog(15)
        say("диалог:", title, h)
        if not h:
            raise RuntimeError("диалог не открылся")
        place(h)
        d = s.dlg_ui(h)
        clicked = False
        for t in d.descendants(control_type="TabItem"):
            if t.window_text().strip() == "Затраты":
                t.click_input()
                clicked = True
                break
        say("вкладка Затраты:", clicked)
        time.sleep(1.5)
        place(h)
        say("OK 40", capture(h, os.path.join(paths.SHOTS, "40_ставка_ресурса.png")))
        place(h, -4000, -4000)
        s.dlg_button(h, "Отмена")
    finally:
        s.close_all()
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
