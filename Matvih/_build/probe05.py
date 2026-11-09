"""Раскрытие списка «Поиск превышений доступности» и выбор пункта."""
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
    h = None
    try:
        s.menu("Сервис", "Выравнивание загрузки ресурсов...")
        h, title = s.wait_dialog(20)
        say("диалог:", title, h)
        d = s.dlg_ui(h)
        combo = None
        for e in d.descendants(control_type="ComboBox"):
            if "Поиск превышений" in e.window_text():
                combo = e
                break
        say("до:", combo.selected_text())
        try:
            combo.expand()
            say("раскрыт")
        except Exception as e:
            say("expand:", str(e)[:120])
        time.sleep(1.0)
        for e in combo.descendants():
            say("   ", e.element_info.control_type, repr(e.window_text()))
        target = None
        for e in combo.descendants(control_type="ListItem"):
            if e.window_text().strip() == "по дням":
                target = e
                break
        if target is not None:
            try:
                target.select()
                say("выбран по дням")
            except Exception as e:
                say("select item:", str(e)[:120])
        time.sleep(1.0)
        try:
            combo.collapse()
        except Exception:
            pass
        time.sleep(0.8)
        say("после:", combo.selected_text())
        say("shot", capture(h, os.path.join(OUT, "_probe05.png")))
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
