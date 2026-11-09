"""Пересъёмка диалогов 11, 13, 15, 16, 22."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, capture, say

OUT = paths.SHOTS


def find(s, h, ctype, text, startswith=False):
    d = s.dlg_ui(h)
    if d is None:
        return None
    for e in d.descendants(control_type=ctype):
        t = e.window_text().strip()
        if (t.startswith(text) if startswith else t == text):
            return e
    return None


def invoke_menu_item(s, text):
    for e in s.mp.descendants(control_type="MenuItem"):
        try:
            if e.window_text().strip() == text:
                e.invoke()
                return True
        except Exception:
            continue
    return False


def shot(s, name, opener, after=None, delay=2.0):
    path = os.path.join(OUT, name + ".png")
    h = None
    try:
        s.pre = set()
        opener()
        h, title = s.wait_dialog(20)
        if not h:
            raise RuntimeError("диалог не найден")
        say("  диалог:", title, h)
        time.sleep(1.2)
        if after:
            after(h)
            time.sleep(1.2)
        size = capture(h, path)
        say("OK %-24s %s" % (name, size))
        return True
    except Exception as e:
        say("FAIL %-24s %s" % (name, str(e)[:140]))
        return False
    finally:
        if h:
            try:
                s.dlg_button(h, "Отмена")
            except Exception as e:
                say("  cancel:", str(e)[:80])
        time.sleep(1.0)
        for hh, cls, t in __import__("reshoot_fixed").windows():
            pass


def main():
    s = Shot()
    s.show = lambda: None
    try:
        s.app.ViewApply("Диаграмма Ганта")
        time.sleep(1.0)

        # 11 - обновление задач (задача 23, 90%)
        s.app.SelectTaskField(23, "Name", False)
        time.sleep(0.8)
        shot(s, "11_обновить_задачи",
             lambda: s.menu("Сервис", "Отслеживание", "Обновить задачи..."))

        # 16 - масштаб
        shot(s, "16_масштаб", lambda: s.menu("Вид", "Масштаб..."),
             after=lambda h: select_radio(s, h, "1 месяц"))

        # контекстная вкладка «Формат диаграммы Ганта»
        s.ribbon_tab("Формат диаграммы Ганта")
        time.sleep(1.0)

        # 13 - мастер диаграмм Ганта
        shot(s, "13_мастер_диаграмм_ганта",
             lambda: invoke_menu_item(s, "Мастер диаграмм Ганта..."),
             after=lambda h: select_radio(s, h, "Критический путь"))

        # 15 - стили текста, элемент «Веха»
        s.app.SelectTaskField(10, "Name", False)
        time.sleep(0.6)
        shot(s, "15_стили_текста",
             lambda: invoke_menu_item(s, "Стили текста..."),
             after=lambda h: select_combo(s, h, "Изменяемый элемент", "Веха"))

        # 22 - формат отрезка для задачи 29
        s.app.SelectTaskField(29, "Name", False)
        time.sleep(0.6)
        shot(s, "22_формат_отрезка",
             lambda: invoke_menu_item(s, "Формат отрезка..."))
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


def select_radio(s, h, text):
    e = find(s, h, "RadioButton", text)
    if e is None:
        say("  радиокнопка не найдена:", text)
        return False
    try:
        e.select()
        say("  радио:", text, "OK")
        return True
    except Exception as exc:
        say("  радио:", str(exc)[:80])
        return False


def select_combo(s, h, name, value):
    combo = None
    for e in s.dlg_ui(h).descendants(control_type="ComboBox"):
        if e.window_text().startswith(name):
            combo = e
            break
    if combo is None:
        say("  комбо не найдено:", name)
        return False
    say("  комбо было:", combo.selected_text())
    try:
        combo.expand()
        time.sleep(0.8)
        for it in combo.descendants(control_type="ListItem"):
            if it.window_text().strip() == value:
                it.select()
                say("  выбрано:", value)
                break
        combo.collapse()
    except Exception as exc:
        say("  combo:", str(exc)[:90])
    time.sleep(0.6)
    say("  комбо стало:", combo.selected_text())
    return True


if __name__ == "__main__":
    main()
