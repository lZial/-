"""Разведка диалога «Повторяющаяся задача»."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say


def main():
    s = Shot()
    try:
        s.menu("Вставка", "Повторяющаяся задача...")
        h, title = s.wait_dialog(timeout=25)
        say("dialog:", title, h)
        if not h:
            return
        d = s.dlg_ui(h)
        for e in d.descendants():
            try:
                ct = e.element_info.control_type
            except Exception:
                ct = "?"
            try:
                tx = e.window_text()
            except Exception:
                tx = ""
            try:
                val = e.get_value()
            except Exception:
                val = ""
            say("%-12s | %-40s | %s" % (ct, tx[:40], str(val)[:40]))
    finally:
        try:
            s.close_all()
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
