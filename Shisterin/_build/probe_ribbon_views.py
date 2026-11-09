"""Разведка ленты «Вид»: какие элементы отвечают за представления ресурсов."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say


def main():
    s = Shot()
    try:
        s.ribbon_tab("Вид")
        time.sleep(1.2)
        for ct in ("Button", "SplitButton"):
            for b in s.mp.descendants(control_type=ct):
                try:
                    t = b.window_text().strip()
                except Exception:
                    continue
                if "ресурс" in t.lower():
                    try:
                        en = b.is_enabled()
                    except Exception:
                        en = "?"
                    say(ct, repr(t), "enabled=", en)
        say("--- пункты меню (если открыты) ---")
        for it in s.mp.descendants(control_type="MenuItem"):
            try:
                t = it.window_text().strip()
                if t:
                    say("MENU", repr(t))
            except Exception:
                pass
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
