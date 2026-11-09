"""Проверка UIA-паттернов для раздела «Расписание» в «Параметры Project»."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, capture, say

OUT = paths.SHOTS


def main():
    s = Shot()
    s.show = lambda: None
    try:
        s.menu("Сервис", "Параметры...")
        h, title = s.wait_dialog(20)
        say("диалог:", title, h)
        d = s.dlg_ui(h)
        item = None
        for e in d.descendants(control_type="ListItem"):
            if e.window_text().strip() == "Расписание":
                item = e
                break
        for name in ("select", "invoke", "set_focus"):
            try:
                getattr(item, name)()
                say(name, "OK")
            except Exception as e:
                say(name, "FAIL", str(e)[:160])
            time.sleep(1.0)
        time.sleep(1.5)
        for e in d.descendants(control_type="Text"):
            try:
                t = e.window_text()
                if t and ("асов" in t or "расписан" in t.lower()):
                    say("текст:", t)
            except Exception:
                pass
        say("shot", capture(h, os.path.join(OUT, "_probe_21b.png")))
        s.dlg_button(h, "Отмена")
    finally:
        s.close_all()
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
