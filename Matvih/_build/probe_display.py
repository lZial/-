"""Дамп раздела «Отображение» диалога «Параметры Project»."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say


def main():
    s = Shot()
    s.show = lambda: None
    try:
        s.menu("Сервис", "Параметры...")
        h, title = s.wait_dialog(20)
        say("диалог:", title, h)
        d = s.dlg_ui(h)
        for e in d.descendants(control_type="ListItem"):
            if e.window_text().strip() == "Отображение":
                e.select()
                say("Отображение выбрано")
                break
        time.sleep(2.0)
        for e in d.descendants():
            try:
                t = e.window_text().strip()
                ct = e.element_info.control_type
                if t and ct in ("CheckBox", "Button", "ComboBox", "Edit", "Text"):
                    say("%-12s %r" % (ct, t[:70]))
            except Exception:
                pass
        s.dlg_button(h, "Отмена")
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
