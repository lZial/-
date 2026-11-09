"""Разведка элементов масштаба в режиме отчета."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reshoot_fixed import Shot, say


def find(root, name, ctype=None):
    for e in root.descendants():
        try:
            if e.window_text().strip() != name:
                continue
            if ctype and getattr(e.element_info, "control_type", "") != ctype:
                continue
            return e
        except Exception:
            pass
    return None


def main():
    s = Shot()
    try:
        s.show()
        s.ribbon_tab("Отчет")
        time.sleep(1.0)
        g = find(s.mp, "Панели мониторинга", "MenuItem")
        g.click_input()
        time.sleep(1.2)
        t = find(s.mp, "Обзор проекта", "ListItem")
        t.click_input()
        time.sleep(12)
        say("--- элементы статуса/масштаба ---")
        for e in s.mp.descendants():
            try:
                ct = getattr(e.element_info, "control_type", "")
                t = e.window_text().strip()
                if ct in ("Slider", "Spinner", "Button") and (
                        "масштаб" in t.lower() or ct in ("Slider", "Spinner")
                        or t in ("Уменьшить", "Увеличить")):
                    r = e.rectangle()
                    extra = ""
                    try:
                        extra = " value=%s" % e.get_value()
                    except Exception:
                        pass
                    say(ct, repr(t), (r.left, r.top, r.right, r.bottom), extra)
            except Exception:
                pass
        # COM-варианты
        for expr in ("s.app.ActiveWindow.Zoom", "s.app.ActiveWindow.ZoomTimescale"):
            try:
                say(expr, "=", eval(expr))
            except Exception as e:
                say(expr, "ERR", str(e)[:90])
        for call in ("s.app.ZoomReport(80)", "s.app.ActiveWindow.Zoom = 80"):
            try:
                eval(call)
                say(call, "OK")
                time.sleep(2)
                say("  shot test")
                break
            except Exception as e:
                say(call, "ERR", str(e)[:90])
    finally:
        try:
            s.app.ActiveProject.Saved = True
        except Exception:
            pass
        time.sleep(0.5)
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
