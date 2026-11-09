"""Создание повторяющейся задачи «Совещание» в проекте."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say


def by_text(items, text, exact=True):
    for e in items:
        try:
            t = e.window_text().strip()
        except Exception:
            continue
        if (t == text) if exact else (text in t):
            return e
    return None


def main():
    s = Shot()
    try:
        s.menu("Вставка", "Повторяющаяся задача...")
        h, title = s.wait_dialog(timeout=25)
        if not h:
            raise RuntimeError("диалог не открыт")
        say("диалог:", title)
        d = s.dlg_ui(h)
        edits = list(d.descendants(control_type="Edit"))
        radios = list(d.descendants(control_type="RadioButton"))
        checks = list(d.descendants(control_type="CheckBox"))

        # рабочее время
        r = by_text(radios, "Рабочие часы:")
        if r:
            r.select()
            time.sleep(0.5)

        # название
        name_edit = None
        for e in edits:
            try:
                if not e.get_value():
                    name_edit = e
                    break
            except Exception:
                pass
        if name_edit is None:
            raise RuntimeError("нет поля названия")
        name_edit.set_edit_text("Совещание")
        say("название задано")

        # длительность 1 ч
        dur = by_text(edits, "1д")
        if dur is None:
            raise RuntimeError("нет поля длительности")
        dur.set_edit_text("1ч")
        say("длительность 1ч")

        # еженедельно
        r = by_text(radios, "Еженедельно")
        if r:
            r.select()
            time.sleep(0.8)
            radios = list(d.descendants(control_type="RadioButton"))
            checks = list(d.descendants(control_type="CheckBox"))

        # день недели: только пятница
        for c in checks:
            try:
                nm = c.window_text().strip()
            except Exception:
                continue
            if nm.endswith("ям") or nm.endswith("ам"):
                want = (nm == "пятницам")
                if bool(c.get_toggle_state()) != want:
                    c.toggle()
                    time.sleep(0.25)
        say("день недели: пятница")

        # пределы повторения: даты
        r = by_text(radios, "Окончание:")
        if r is None:
            raise RuntimeError("нет переключателя окончания")
        r.select()
        time.sleep(0.8)
        edits = list(d.descendants(control_type="Edit"))
        start_edit = end_edit = None
        for e in edits:
            try:
                v = str(e.get_value())
            except Exception:
                continue
            if "03.02" in v:
                start_edit = e
            elif "18.08" in v:
                end_edit = e
        if start_edit is None or end_edit is None:
            raise RuntimeError("не найдены поля дат: %s"
                               % [str(e.get_value())[:20] for e in edits])
        start_edit.set_edit_text("07.02.25")
        time.sleep(0.4)
        end_edit.set_edit_text("15.08.25")
        time.sleep(0.5)
        say("даты:", start_edit.get_value(), "-", end_edit.get_value())

        ok = by_text(list(d.descendants(control_type="Button")), "ОК")
        if ok is None:
            raise RuntimeError("нет кнопки ОК")
        ok.invoke()
        time.sleep(3.0)

        # проверка
        pr = s.app.ActiveProject
        tasks = [t.Name for t in pr.Tasks if "Совещание" in str(t.Name)]
        say("задач всего:", pr.Tasks.Count, "| совещаний:", len(tasks))
        s.app.FileSave()
        say("сохранено")
    finally:
        try:
            s.close_all()
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
