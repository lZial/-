"""Диагностика окна «Масштаб»."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, capture, say

OUT = paths.SHOTS


def radios(d):
    out = []
    for e in d.descendants(control_type="RadioButton"):
        try:
            out.append((e.window_text().strip(), e.is_selected()))
        except Exception as exc:
            out.append((e.window_text().strip(), "err:" + str(exc)[:30]))
    return out


def main():
    s = Shot()
    s.show = lambda: None
    h = None
    try:
        s.menu("Вид", "Масштаб...")
        h, title = s.wait_dialog(20)
        say("диалог:", title, h)
        d = s.dlg_ui(h)
        say("до:", radios(d))
        target = None
        for e in d.descendants(control_type="RadioButton"):
            if e.window_text().strip() == "1 месяц":
                target = e
        if target is None:
            raise RuntimeError("нет радио 1 месяц")
        say("rect:", target.rectangle())
        target.select()
        time.sleep(1.2)
        say("после:", radios(d))
        say("shot", capture(h, os.path.join(OUT, "_probe16.png")))
    except Exception as exc:
        say("FAIL:", str(exc)[:160])
    finally:
        if h:
            try:
                s.dlg_button(h, "Отмена")
            except Exception as e:
                say("cancel:", str(e)[:80])
        time.sleep(1.0)
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
