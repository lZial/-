# -*- coding: utf-8 -*-
"""Досъёмка снимков Шистерина: 28, 31, 32, 37, 39, 41, 42.

Каждый кадр снимается в одном сеансе, ошибки не прерывают остальные.
Запуск: python _reshoot_sh_rest.py [ключ ...]
"""
import ctypes
import os
import sys
import time
import traceback

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, capture, rect, say
from winfocus import keys_to_pid

user32 = ctypes.windll.user32
SWP_NOACTIVATE = 0x0010
HWND_BOTTOM = 1
SWP_NOZORDER = 0x0004
OFF = (-4000, -4000)


def capture_onscreen(s, hwnd, path, delay=2.0):
    l, t, r, b = rect(hwnd)
    w, hh = r - l, b - t
    user32.SetWindowPos(hwnd, HWND_BOTTOM, 0, 0, w, hh, SWP_NOACTIVATE)
    time.sleep(delay)
    size = capture(hwnd, path)
    user32.SetWindowPos(hwnd, 0, OFF[0], OFF[1], w, hh, SWP_NOZORDER)
    time.sleep(0.5)
    return size


def zoom_entire(s):
    """Вид -> Масштаб... -> «Весь проект» -> OK."""
    if not s.menu("Вид", "Масштаб..."):
        raise RuntimeError("нет меню Вид/Масштаб")
    h, title = s.wait_dialog(10)
    if not h:
        raise RuntimeError("нет диалога Масштаб")
    d = s.dlg_ui(h)
    done = False
    if d is not None:
        for e in d.descendants(control_type="RadioButton"):
            try:
                if "роект" in e.window_text():
                    e.select()
                    done = True
                    break
            except Exception:
                pass
    say("  «Весь проект»:", done)
    time.sleep(0.5)
    s.dlg_button(h, "ОК")
    time.sleep(1.5)


def do_28(s):
    s.app.ViewApply("Сетевой график")
    time.sleep(2.0)
    zoom_entire(s)
    s.hide()
    time.sleep(0.5)
    say("OK 28", capture_onscreen(s, s.hwnd,
                                  os.path.join(paths.SHOTS, "28_сетевой_график.png")))


def do_31(s):
    s.app.ViewApply("Использование ресурсов")
    time.sleep(2.0)
    s.hide()
    time.sleep(0.5)
    say("OK 31", capture(s.hwnd, os.path.join(paths.SHOTS,
                                              "31_использование_ресурсов.png")))


def do_32(s):
    s.app.ViewApply("Лист ресурсов")
    time.sleep(1.8)
    s.app.SelectResourceField(6, "Name", False)
    time.sleep(0.6)
    say("32 ресурс:", s.app.ActiveCell.Text)
    s.app.ViewApply("График ресурсов")
    time.sleep(2.0)
    zoom_entire(s)
    s.hide()
    time.sleep(0.5)
    say("OK 32", capture_onscreen(s, s.hwnd,
                                  os.path.join(paths.SHOTS, "32_график_ресурса.png")))


def shot_task_tab(s, fragment, tid, tab, name, path):
    s.app.ViewApply("Диаграмма Ганта")
    time.sleep(1.2)
    try:
        s.app.FilterClear()
    except Exception:
        pass
    s.app.OutlineShowAllTasks()
    time.sleep(0.8)
    s.show()
    time.sleep(0.6)
    try:
        user32.SetForegroundWindow(s.hwnd)
    except Exception:
        pass
    try:
        s.mp.set_focus()
    except Exception:
        pass
    time.sleep(0.4)
    # переход к задаче по ID через диалог «Переход»
    s.pre = set()
    keys_to_pid("{F5}", s.pid)
    hg, tg = s.wait_dialog(8)
    if not hg:
        raise RuntimeError("нет диалога Переход")
    try:
        user32.SetForegroundWindow(hg)
    except Exception:
        pass
    time.sleep(0.4)
    keys_to_pid("^a", s.pid)
    keys_to_pid(str(tid), s.pid)
    time.sleep(0.4)
    keys_to_pid("{ENTER}", s.pid)
    time.sleep(1.5)
    try:
        say("  задача:", s.app.ActiveCell.Task.ID, s.app.ActiveCell.Task.Name)
    except Exception:
        say("  задача: (нет данных)")
    s.pre = set()
    keys_to_pid("+{F2}", s.pid)
    h, title = s.wait_dialog()
    say("  диалог:", title)
    if not h:
        raise RuntimeError("нет диалога задачи")
    # переключение на нужную вкладку: select + click (select иногда не срабатывает)
    d = s.dlg_ui(h)
    switched = False
    if d is not None:
        for t in d.descendants(control_type="TabItem"):
            try:
                if t.window_text().strip() == tab:
                    try:
                        t.select()
                    except Exception:
                        pass
                    time.sleep(0.5)
                    try:
                        t.click_input()
                    except Exception:
                        pass
                    switched = True
                    break
            except Exception:
                continue
    say("  вкладка", tab, ":", switched)
    time.sleep(1.2)
    say("OK", name, capture(h, path))
    s.close_all()


def shot_stats(s, name, path):
    s.pre = set()
    s.show()
    if not s.menu("Проект", "Сведения о проекте..."):
        raise RuntimeError("нет меню Сведения о проекте")
    h, title = s.wait_dialog()
    say("  диалог:", title)
    if not h:
        raise RuntimeError("нет диалога сведений")
    if not s.dlg_button(h, "Статистика"):
        raise RuntimeError("нет кнопки Статистика")
    h2, t2 = s.wait_dialog()
    say("  статистика:", t2)
    if not h2:
        raise RuntimeError("нет окна статистики")
    time.sleep(1.0)
    say("OK", name, capture(h2, path))
    s.close_all()


STEPS = {
    "28": lambda s: do_28(s),
    "31": lambda s: do_31(s),
    "32": lambda s: do_32(s),
    "37": lambda s: shot_task_tab(s, "Создание репозитория", 8, "Предшественники",
                                  "37", os.path.join(paths.SHOTS, "37_связь_нн.png")),
    "39": lambda s: shot_stats(s, "39", os.path.join(paths.SHOTS, "39_статистика_проекта.png")),
    "42": lambda s: shot_task_tab(s, "Создание репозитория", 8, "Дополнительно",
                                  "42", os.path.join(paths.SHOTS, "42_тип_задачи.png")),
    "41": None,
}


def do_41(s):
    s.app.FileOpen(paths.EXP_MPP)
    time.sleep(5)
    try:
        s.wait_ready()
    except Exception:
        pass
    shot_stats(s, "41", os.path.join(paths.SHOTS, "41_затраты_после_изменения.png"))


def main():
    keys = sys.argv[1:] or list(STEPS.keys())
    s = Shot()
    try:
        for k in keys:
            say("=== шаг", k)
            try:
                if k == "41":
                    do_41(s)
                else:
                    STEPS[k](s)
            except Exception as e:
                say("FAIL", k, str(e)[:180])
                traceback.print_exc()
                try:
                    s.close_all()
                except Exception:
                    pass
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
