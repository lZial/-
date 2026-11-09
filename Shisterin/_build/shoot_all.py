"""Пакетная пересъёмка скриншотов для отчёта по новой теме.

Окно MS Project постоянно находится за пределами экрана; снимки делаются
через PrintWindow. Представления, которые не отрисовываются вне экрана
(сетевой график, календарь, график ресурсов), на 2-3 секунды опускаются
в низ z-порядка (HWND_BOTTOM) и затем возвращаются за экран.

Запуск: python shoot_all.py <этап>
    views    - 26, 27, 28, 29, 30, 31, 32
    dialogs  - 01, 02, 03, 05, 06, 20, 21, 39, 42
    tabs     - 33, 34, 35, 36
    exp      - 40, 41
"""
import ctypes
import os
import sys
import time
import traceback
from ctypes import wintypes

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import (MAIN_CLASS, OFF, Shot, capture, move_off, pid_of,
                           rect, say, windows)
from shoot_gantt import stitch

user32 = ctypes.windll.user32
OUT = paths.SHOTS
HWND_BOTTOM = 1
SWP_NOSIZE, SWP_NOACTIVATE = 0x0001, 0x0010
SWP_NOZORDER = 0x0004


def resize(s, w=1500, h=1000):
    user32.SetWindowPos(s.hwnd, 0, OFF[0], OFF[1], w, h, SWP_NOZORDER)
    time.sleep(1.2)


def close_stray(s):
    """Закрывает только окна нашего процесса (WM_CLOSE по PID)."""
    for h, cls, title in windows():
        if cls == MAIN_CLASS or pid_of(h) != s.pid:
            continue
        try:
            user32.PostMessageW(h, 0x0010, 0, 0)
        except Exception:
            pass
    time.sleep(0.6)


def capture_onscreen(s, hwnd, path, delay=2.2):
    """Окно на 2 секунды в низ z-порядка: элементы успевают перерисоваться."""
    l, t, r, b = rect(hwnd)
    w, hh = r - l, b - t
    user32.SetWindowPos(hwnd, HWND_BOTTOM, 0, 0, w, hh, SWP_NOACTIVATE)
    time.sleep(delay)
    size = capture(hwnd, path)
    user32.SetWindowPos(hwnd, 0, OFF[0], OFF[1], w, hh, SWP_NOZORDER)
    time.sleep(0.5)
    return size


def select_task(s, tid):
    s.app.SelectTaskField(tid, "Name", False)
    time.sleep(0.7)
    return s.app.ActiveCell.Text


def clear_view(s):
    try:
        s.app.FilterClear()
    except Exception:
        pass
    try:
        s.app.OutlineShowAllTasks()
    except Exception:
        pass
    time.sleep(0.6)


# ------------------------------------------------------------------ виды
def view_task_usage(s):
    s.app.ViewApply("Использование задач")
    time.sleep(2.0)
    time.sleep(1.2)
    p = os.path.join(OUT, "27_использование_задач.png")
    say("27", capture(s.hwnd, p))


def view_resource_sheet(s):
    resize(s, 1500, 1200)
    s.app.ViewApply("Лист ресурсов")
    time.sleep(2.0)
    p = os.path.join(OUT, "30_лист_ресурсов.png")
    say("30", capture(s.hwnd, p))
    resize(s)


def view_resource_usage(s):
    s.app.ViewApply("Использование ресурсов")
    time.sleep(2.0)
    try:
        s.app.ZoomTimescale(Entire=True)
        say("31: масштаб весь проект")
    except Exception as e:
        say("31 zoom:", str(e)[:90])
    time.sleep(1.5)
    p = os.path.join(OUT, "31_использование_ресурсов.png")
    say("31", capture(s.hwnd, p))


def view_network(s):
    s.app.ViewApply("Сетевой график")
    time.sleep(2.0)
    try:
        s.app.Zoom(Entire=True)
        say("28: масштаб весь проект")
    except Exception as e:
        say("28 Zoom:", str(e)[:90])
    time.sleep(1.5)
    p = os.path.join(OUT, "28_сетевой_график.png")
    say("28", capture_onscreen(s, s.hwnd, p))


def view_calendar(s):
    s.app.ViewApply("Календарь")
    time.sleep(2.5)
    p = os.path.join(OUT, "29_календарь.png")
    say("29", capture_onscreen(s, s.hwnd, p))


def view_resource_graph(s):
    s.app.ViewApply("Лист ресурсов")
    time.sleep(1.8)
    s.app.SelectResourceField(6, "Name", False)
    time.sleep(0.6)
    say("32 ресурс:", s.app.ActiveCell.Text)
    s.app.ViewApply("График ресурсов")
    time.sleep(2.0)
    try:
        s.app.ZoomTimescale(Entire=True)
    except Exception as e:
        say("32 zoom:", str(e)[:90])
    time.sleep(1.5)
    p = os.path.join(OUT, "32_график_ресурса.png")
    say("32", capture_onscreen(s, s.hwnd, p))


def stage_views(s):
    resize(s)
    clear_view(s)
    view_task_usage(s)
    view_resource_sheet(s)
    view_resource_usage(s)
    view_network(s)
    view_calendar(s)
    view_resource_graph(s)
    # 26 - диаграмма Ганта только со сводными задачами
    s.app.ViewApply("Диаграмма Ганта")
    time.sleep(2.0)
    clear_view(s)
    try:
        s.app.FilterApply("Суммарные задачи", False)
        say("фильтр: Суммарные задачи")
    except Exception as e:
        say("фильтр:", str(e)[:90])
    time.sleep(1.5)
    s.app.ZoomTimescale(Entire=True)
    time.sleep(2.5)
    s.app.ViewApply("Диаграмма Ганта")
    time.sleep(1.5)
    try:
        s.app.ZoomTimescale(Entire=True)
    except Exception:
        pass
    time.sleep(1.5)
    raw = os.path.join(OUT, "_gantt_raw.png")
    say("26 raw", capture(s.hwnd, raw))
    stitch(raw, os.path.join(OUT, "26_диаграмма_ганта.png"))
    try:
        os.remove(raw)
    except Exception:
        pass


# ------------------------------------------------------------------ диалоги
DEF_TABS = ("TabItem", "ListItem")


def dialog_tab(s, h, tab):
    d = s.dlg_ui(h)
    if d is None:
        return False
    for ct in DEF_TABS:
        for e in d.descendants(control_type=ct):
            try:
                if e.window_text().strip() == tab:
                    e.select()
                    return True
            except Exception:
                continue
    return False


def dialog_combo(s, h, name, value):
    d = s.dlg_ui(h)
    if d is None:
        return False
    for e in d.descendants(control_type="ComboBox"):
        try:
            if e.window_text().strip() == name:
                e.select(value)
                return True
        except Exception as ex:
            say("   combo %s: %s" % (name, str(ex)[:80]))
    return False


def shot_dialog(s, name, opener, tab=None, checkbox=None, combo=None,
                delay=1.8):
    path = os.path.join(OUT, name + ".png")
    try:
        s.pre = set(h for h, c, t in windows())
        opener()
        h, title = s.wait_dialog(22)
    except Exception as e:
        say("FAIL %-26s %s" % (name, str(e)[:130]))
        close_stray(s)
        return False
    if not h:
        say("FAIL %-26s диалог не найден" % name)
        close_stray(s)
        return False
    time.sleep(1.2)
    if tab:
        done = dialog_tab(s, h, tab)
        say("  вкладка %s: %s" % (tab, done))
        time.sleep(1.2)
    if combo:
        cname, cvalue = combo
        done = dialog_combo(s, h, cname, cvalue)
        say("  список %s = %s: %s" % (cname, cvalue, done))
        time.sleep(1.0)
    if checkbox:
        d = s.dlg_ui(h)
        done = False
        if d is not None:
            for e in d.descendants(control_type="CheckBox"):
                try:
                    if e.window_text().strip() == checkbox:
                        if not e.get_toggle_state():
                            e.toggle()
                        done = True
                        break
                except Exception:
                    pass
        say("  флажок %s: %s" % (checkbox, done))
        time.sleep(1.0)
    size = capture_onscreen(s, h, path)
    say("OK %-26s %s %r" % (name, size, title[:40]))
    s.dlg_button(h, "Отмена")
    time.sleep(1.0)
    close_stray(s)
    return True


def stage_dialogs(s):
    resize(s)
    clear_view(s)

    # 01 - сведения о проекте
    shot_dialog(s, "01_сведения_о_проекте",
                lambda: s.menu("Проект", "Сведения о проекте..."))

    # 02 - сведения о задаче (обучение модели)
    select_task(s, 29)
    shot_dialog(s, "02_сведения_о_задаче",
                lambda: s.menu("Проект", "Сведения о задаче..."), tab="Общие")

    # 03 - заметки задачи с описанием риска
    select_task(s, 29)
    shot_dialog(s, "03_заметки_задачи",
                lambda: s.menu("Проект", "Заметки задачи..."))

    # 42 - дополнительно: тип задачи
    select_task(s, 29)
    shot_dialog(s, "42_тип_задачи",
                lambda: s.menu("Проект", "Сведения о задаче..."),
                tab="Дополнительно")

    # 05 - выравнивание загрузки ресурсов
    shot_dialog(s, "05_выравнивание_ресурсов",
                lambda: s.menu("Сервис", "Выравнивание загрузки ресурсов..."),
                checkbox="Выравнивание только в пределах имеющегося резерва",
                combo=("Поиск превышений доступности", "по дням"))

    # 06 - назначение ресурсов
    select_task(s, 29)
    shot_dialog(s, "06_назначить_ресурсы",
                lambda: s.menu("Сервис", "Назначить ресурсы..."))

    # 20 - гиперссылка на реестр рисков
    select_task(s, 50)
    shot_dialog(s, "20_гиперссылка",
                lambda: s.menu("Вставка", "Гиперссылка..."))

    # 21 - параметры, раздел «Расписание»
    shot_dialog(s, "21_параметры",
                lambda: s.menu("Сервис", "Параметры..."), tab="Расписание")

    # 39 - статистика проекта (через кнопку в «Сведения о проекте»)
    shot_stats(s)


def shot_stats(s, name="39_статистика_проекта"):
    path = os.path.join(OUT, name + ".png")
    try:
        s.pre = set(h for h, c, t in windows())
        s.menu("Проект", "Сведения о проекте...")
        h1, t1 = s.wait_dialog(22)
        if not h1:
            raise RuntimeError("нет окна сведений о проекте")
        time.sleep(1.0)
        d = s.dlg_ui(h1)
        clicked = False
        for b in d.descendants(control_type="Button"):
            try:
                if b.window_text().strip().startswith("Статистика"):
                    s.pre = set(h for h, c, t in windows())
                    b.invoke()
                    clicked = True
                    break
            except Exception:
                pass
        if not clicked:
            raise RuntimeError("кнопка «Статистика...» не найдена")
        h2, t2 = s.wait_dialog(22)
        if not h2:
            raise RuntimeError("нет окна статистики")
        time.sleep(1.2)
        size = capture_onscreen(s, h2, path)
        say("OK %-26s %s %r" % (name, size, t2[:40]))
        s.dlg_button(h2, "Закрыть")
        time.sleep(0.8)
        s.dlg_button(h1, "Отмена")
        time.sleep(0.8)
    except Exception as e:
        say("FAIL %-26s %s" % (name, str(e)[:130]))
    close_stray(s)


# ------------------------------------------------------------------ вкладки
def stage_tabs(s):
    resize(s)
    from reshoot_fixed import shot_tab
    for name, tab in (("33_вкладка_задача", "Задача"),
                      ("34_вкладка_ресурс", "Ресурс"),
                      ("35_вкладка_проект", "Проект"),
                      ("36_вкладка_отчет", "Отчет")):
        size = shot_tab(s, name, tab)
        say("OK", name, size)


# ------------------------------------------------------------------ эксперимент
def stage_exp(s):
    resize(s)
    s.app.FileOpen(paths.EXP_MPP)
    time.sleep(6)
    close_stray(s)
    clear_view(s)

    # 40 - ставка ML-инженера
    s.app.ViewApply("Лист ресурсов")
    time.sleep(1.6)
    s.app.SelectResourceField(6, "Name", False)
    time.sleep(0.6)
    say("40 ресурс:", s.app.ActiveCell.Text)
    s.ribbon_tab("Ресурс")
    opened = False
    for b in s.mp.descendants(control_type="Button"):
        try:
            if b.window_text().strip() == "Сведения...":
                b.invoke()
                opened = True
                break
        except Exception:
            pass
    if not opened:
        raise RuntimeError("кнопка «Сведения...» не найдена")
    h, title = s.wait_dialog(20)
    say("40 диалог:", title)
    time.sleep(1.0)
    d = s.dlg_ui(h)
    for t in d.descendants(control_type="TabItem"):
        try:
            if t.window_text().strip() == "Затраты":
                t.select()
                break
        except Exception:
            pass
    time.sleep(1.5)
    say("OK 40", capture_onscreen(s, h, os.path.join(OUT, "40_ставка_ресурса.png")))
    s.dlg_button(h, "Отмена")
    time.sleep(1.0)
    close_stray(s)

    # 41 - статистика экспериментальной копии
    shot_stats(s, "41_затраты_после_изменения")
    try:
        s.app.FileClose(0)          # закрыть экспериментальную копию
        time.sleep(2.0)
    except Exception as e:
        say("закрытие эксперимента:", str(e)[:80])


def stage_fix(s):
    """Пересъёмка отдельных кадров после правок."""
    resize(s)
    clear_view(s)
    view_resource_sheet(s)
    view_resource_usage(s)
    shot_dialog(s, "05_выравнивание_ресурсов",
                lambda: s.menu("Сервис", "Выравнивание загрузки ресурсов..."),
                checkbox="Выравнивание только в пределах имеющегося резерва",
                combo=("Поиск превышений доступности", "по дням"))
    shot_dialog(s, "21_параметры",
                lambda: s.menu("Сервис", "Параметры..."), tab="Расписание")
    shot_stats(s)


STAGES = {
    "views": stage_views,
    "dialogs": stage_dialogs,
    "tabs": stage_tabs,
    "exp": stage_exp,
    "fix": stage_fix,
}


def main():
    stage = sys.argv[1] if len(sys.argv) > 1 else "views"
    s = Shot()
    s.show = lambda: None
    try:
        for _ in range(40):
            if s.wait_ready(3):
                break
            close_stray(s)
        close_stray(s)
        STAGES[stage](s)
    except Exception:
        traceback.print_exc()
    finally:
        close_stray(s)
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
