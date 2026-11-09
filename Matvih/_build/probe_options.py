"""Диагностика левой панели диалога «Параметры Project»."""
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
        for e in d.descendants():
            try:
                r = e.rectangle()
                if r.left < 320:
                    say("%-16s %-28r rect=%s" % (
                        e.element_info.control_type, e.window_text()[:28],
                        (r.left, r.top, r.right, r.bottom)))
            except Exception:
                pass
        s.dlg_button(h, "Отмена")
    finally:
        s.close_all()
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
