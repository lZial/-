# -*- coding: utf-8 -*-
"""Переставляет повторяющуюся задачу «Совещание» в конец списка задач.

В текущем файле серия оказалась в начале (ID 1-29), из-за чего сдвинулись
ID основных задач и диаграмма Ганта показывала совещания. Скрипт удаляет
серию и вставляет её заново после последней задачи.
"""
import os
import sys
import time
import traceback

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


def insert_recurring(s):
    s.menu("Вставка", "Повторяющаяся задача...")
    h, title = s.wait_dialog(timeout=25)
    if not h:
        raise RuntimeError("диалог не открыт")
    say("диалог:", title)
    d = s.dlg_ui(h)
    edits = list(d.descendants(control_type="Edit"))
    radios = list(d.descendants(control_type="RadioButton"))
    checks = list(d.descendants(control_type="CheckBox"))

    r = by_text(radios, "Рабочие часы:")
    if r:
        r.select()
        time.sleep(0.5)

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

    dur = by_text(edits, "1д")
    if dur is None:
        raise RuntimeError("нет поля длительности")
    dur.set_edit_text("1ч")

    r = by_text(radios, "Еженедельно")
    if r:
        r.select()
        time.sleep(0.8)
        radios = list(d.descendants(control_type="RadioButton"))
        checks = list(d.descendants(control_type="CheckBox"))

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
        raise RuntimeError("не найдены поля дат")
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


def main():
    s = Shot()
    try:
        pr = s.app.ActiveProject
        total = pr.Tasks.Count
        say("задач до:", total)
        s.app.ViewApply("Диаграмма Ганта")
        time.sleep(1.5)
        s.app.OutlineShowAllTasks()
        time.sleep(0.8)
        # удалить серию (строка 1 — сводная повторяющейся задачи)
        s.app.SelectTaskField(1, "Name", False)
        time.sleep(0.6)
        say("строка 1:", s.app.ActiveCell.Text)
        s.app.EditDelete()
        time.sleep(2.0)
        # подтверждение удаления серии, если появилось
        try:
            h, t = s.wait_dialog(3)
            if h:
                say("подтверждение:", t)
                for b in s.dlg_ui(h).descendants(control_type="Button"):
                    if b.window_text().strip() in ("Да", "ОК", "Yes"):
                        b.invoke()
                        break
                time.sleep(1.5)
        except Exception:
            pass
        total2 = s.app.ActiveProject.Tasks.Count
        say("задач после удаления:", total2)
        if total2 == total:
            raise RuntimeError("серия не удалилась")
        # вставить в конец
        s.app.OutlineShowAllTasks()
        time.sleep(0.5)
        s.app.SelectTaskField(total2, "Name", False)
        time.sleep(0.6)
        say("последняя строка:", s.app.ActiveCell.Text)
        insert_recurring(s)
        say("задач после вставки:", s.app.ActiveProject.Tasks.Count)
        # показать первые строки
        for i in (1, 2, 3):
            t = s.app.ActiveProject.Tasks.Item(i)
            say(" ", t.ID, str(t.Name)[:50])
        s.app.FileSave()
        say("сохранено")
    except Exception as e:
        say("FAIL", str(e)[:200])
        traceback.print_exc()
    finally:
        try:
            s.close_all()
        except Exception:
            pass
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
