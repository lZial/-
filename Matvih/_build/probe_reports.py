"""Разведка ленты «Отчет» и COM-методов отчетов MS Project."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reshoot_fixed import Shot, say


def dump(el, depth=0, limit=80):
    try:
        kids = el.children()
    except Exception:
        kids = []
    for k in kids[:limit]:
        try:
            say("  " * depth + "%s | %s" % (k.control_type(), k.window_text()))
        except Exception:
            continue
        if depth < 2:
            dump(k, depth + 1, 30)


def main():
    s = Shot()
    try:
        for prop in ("Reports", "ReportPrint", "ReportPrintPreview"):
            try:
                say("COM %s ->" % prop, getattr(s.app, prop))
            except Exception as e:
                say("COM %s err: %s" % (prop, str(e)[:100]))
        s.show()
        s.ribbon_tab("Отчет")
        time.sleep(1.0)
        say("--- элементы вкладки Отчет ---")
        for ct in ("Button", "SplitButton", "DropDownButton", "MenuItem"):
            for b in s.mp.descendants(control_type=ct):
                try:
                    t = b.window_text().strip()
                    if t:
                        say("%s | %s" % (ct, t))
                except Exception:
                    pass
    finally:
        time.sleep(0.5)
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
