"""Разведка галерей отчетов на ленте «Отчет»."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reshoot_fixed import Shot, say


def dump_named(root, label):
    seen = set()
    for el in root.descendants():
        try:
            t = el.window_text().strip()
        except Exception:
            continue
        try:
            ct = el.control_type()
        except Exception:
            ct = getattr(el.element_info, "control_type", "?")
        if not t:
            continue
        key = (ct, t)
        if key in seen:
            continue
        seen.add(key)
        if any(k.lower() in t.lower() for k in
               ("панел", "ресурс", "затрат", "ход", "начало", "друг",
                "последн", "обзор", "отчет", "отчёт", "монитор")):
            say("%s: %s | %s" % (label, ct, t))


def main():
    s = Shot()
    try:
        s.show()
        s.ribbon_tab("Отчет")
        time.sleep(1.0)
        dump_named(s.mp, "ribbon")
        for target in ("Панели мониторинга", "Затраты", "Ресурсы", "Ход выполнения"):
            el = None
            for e in s.mp.descendants():
                try:
                    if e.window_text().strip() == target:
                        el = e
                        break
                except Exception:
                    pass
            if el is None:
                say("нет элемента:", target)
                continue
            say("--- click", target,
                getattr(el.element_info, "control_type", "?"))
            try:
                el.click_input()
            except Exception as ex:
                say("click err", str(ex)[:80])
                try:
                    el.invoke()
                except Exception as ex2:
                    say("invoke err", str(ex2)[:80])
                    continue
            time.sleep(1.5)
            for h, cls, t in __import__("reshoot_fixed").windows():
                if t and any(k in t for k in ("отчет", "отчёт", "Report")):
                    say("window:", cls, t)
            # закрываем галерею повторным нажатием
            try:
                el.click_input()
            except Exception:
                pass
            time.sleep(0.8)
    finally:
        time.sleep(0.5)
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
