"""
Пересъёмка одной исправленной иллюстрации.
Запуск: python reshoot_fixed.py <имя_снимка>

Окно MS Project держится за пределами экрана; снимок делается через
Win32 PrintWindow, элементы активируются UIA-паттернами (select/invoke/toggle).
Каждый снимок снимается в отдельном сеансе MS Project - так надёжнее.
"""
import ctypes
import os
import sys
import time
from ctypes import wintypes

import win32com.client as w
from PIL import Image
from pywinauto import Desktop
from pywinauto.keyboard import send_keys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from winfocus import (FORBIDDEN_CLASSES, keys_to_pid, pid_of, visible_windows)

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
user32.SetProcessDPIAware()
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)

MAIN_CLASS = "JWinproj-WhimperMainClass"
OFF = (-4000, -4000)

# Запрещённые классы окон (оболочка Windows, рабочий стол, панель задач, UWP).
# Определены в winfocus.FORBIDDEN_CLASSES.
# классы, которые просто игнорируются при поиске диалога MS Project
SKIP_CLASSES = FORBIDDEN_CLASSES + ("#32768",)


def say(*a):
    print(*a, flush=True)


def rect(h):
    r = wintypes.RECT()
    user32.GetWindowRect(h, ctypes.byref(r))
    return (r.left, r.top, r.right, r.bottom)


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [("biSize", wintypes.DWORD), ("biWidth", wintypes.LONG),
                ("biHeight", wintypes.LONG), ("biPlanes", wintypes.WORD),
                ("biBitCount", wintypes.WORD), ("biCompression", wintypes.DWORD),
                ("biSizeImage", wintypes.DWORD), ("biXPelsPerMeter", wintypes.LONG),
                ("biYPelsPerMeter", wintypes.LONG), ("biClrUsed", wintypes.DWORD),
                ("biClrImportant", wintypes.DWORD)]


def capture(hwnd, path):
    l, t, r, b = rect(hwnd)
    ww, hh = r - l, b - t
    hdc = user32.GetWindowDC(hwnd)
    mdc = gdi32.CreateCompatibleDC(hdc)
    bmp = gdi32.CreateCompatibleBitmap(hdc, ww, hh)
    gdi32.SelectObject(mdc, bmp)
    user32.PrintWindow(hwnd, mdc, 2)
    bi = BITMAPINFOHEADER()
    bi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bi.biWidth = ww
    bi.biHeight = -hh
    bi.biPlanes = 1
    bi.biBitCount = 32
    bi.biCompression = 0
    buf = ctypes.create_string_buffer(ww * hh * 4)
    gdi32.GetDIBits(mdc, bmp, 0, hh, buf, ctypes.byref(bi), 0)
    img = Image.frombuffer("RGBA", (ww, hh), buf, "raw", "BGRA", 0, 1).convert("RGB")
    img.save(path)
    gdi32.DeleteObject(bmp)
    gdi32.DeleteDC(mdc)
    user32.ReleaseDC(hwnd, hdc)
    return ww, hh


def windows():
    res = []

    def cb(h, l):
        if user32.IsWindowVisible(h):
            cls = ctypes.create_unicode_buffer(256)
            user32.GetClassNameW(h, cls, 256)
            ti = ctypes.create_unicode_buffer(512)
            user32.GetWindowTextW(h, ti, 512)
            res.append((h, cls.value, ti.value))
        return True

    user32.EnumWindows(EnumWindowsProc(cb), 0)
    return res


def move_off(hwnd):
    l, t, r, b = rect(hwnd)
    user32.SetWindowPos(hwnd, 0, OFF[0], OFF[1], r - l, b - t, 0x0040)


def pid_of(hwnd):
    p = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
    return p.value


class Shot(object):
    def __init__(self):
        self.dsk = Desktop(backend="uia")
        self.app = w.Dispatch("MSProject.Application")
        self.app.Visible = True
        self.app.DisplayAlerts = 0
        self.hwnd = None
        t0 = time.time()
        while time.time() - t0 < 40 and self.hwnd is None:
            for h, cls, _ in windows():
                if cls == MAIN_CLASS:
                    self.hwnd = h
                    break
            time.sleep(0.05)
        if self.hwnd is None:
            raise RuntimeError("окно MS Project не найдено")
        move_off(self.hwnd)
        time.sleep(0.4)
        self.app.FileOpen(paths.MPP)
        time.sleep(8)
        move_off(self.hwnd)
        time.sleep(0.5)
        self.mp = [x for x in self.dsk.windows()
                   if x.class_name() == MAIN_CLASS][0]
        self.pid = pid_of(self.hwnd)
        self.pre = set()
        self.wait_ready()
        say("сеанс открыт, окно вне экрана (pid=%s)" % self.pid)

    # ---------------- окно
    def refresh(self):
        """Перезапрашивает UIA-объект окна (после перемещения он устаревает)."""
        try:
            self.mp = [x for x in self.dsk.windows()
                       if x.class_name() == MAIN_CLASS][0]
        except Exception:
            pass

    def show(self):
        l, t, r, b = rect(self.hwnd)
        user32.SetWindowPos(self.hwnd, 0, 0, 0, r - l, b - t, 0x0040)
        time.sleep(0.6)
        try:
            user32.SetForegroundWindow(self.hwnd)
        except Exception:
            pass
        time.sleep(0.4)
        self.refresh()
        time.sleep(0.3)

    def hide(self):
        move_off(self.hwnd)
        time.sleep(0.3)
        self.refresh()

    def act(self, element):
        try:
            element.invoke()
            return True
        except Exception:
            pass
        try:
            element.click_input()
            return True
        except Exception as e:
            say("   act fail:", str(e)[:70])
            return False

    # ---------------- меню
    def menu(self, *path):
        self.show()
        self.pre = set(h for h, c, t in windows())
        mb = None
        for m in self.mp.descendants(control_type="MenuBar"):
            if "меню" in m.window_text():
                mb = m
                break
        if mb is None:
            raise RuntimeError("строка меню не найдена")
        for attempt in range(3):
            try:
                top = [t for t in mb.children()
                       if t.window_text().strip() == path[0]][0]
                if not self.act(top):
                    raise RuntimeError("меню не открылось")
                time.sleep(1.0)
                cur = top
                for label in path[1:]:
                    k = [x for x in cur.children()
                         if x.window_text().strip().strip("[]").startswith(label)][0]
                    if not self.act(k):
                        raise RuntimeError("пункт не открылся")
                    time.sleep(1.0)
                    cur = k
                time.sleep(1.4)
                return True
            except Exception as e:
                say("   menu retry:", str(e)[:70])
                self.show()
                time.sleep(1.2)
        return False

    # ---------------- лента
    def ribbon_tab(self, name):
        """Активирует вкладку ленты (select). При «занятости» приложения - повтор."""
        last = ""
        for attempt in range(6):
            try:
                t = [x for x in self.mp.descendants(control_type="TabItem")
                     if x.window_text().strip() == name][0]
                t.select()
                time.sleep(1.4)
                return True
            except Exception as e:
                last = str(e)[:70]
                time.sleep(2.0)
                self.refresh()
        say("   ribbon_tab[%s] не сработала: %s" % (name, last))
        return False

    def ribbon_button(self, name):
        for ct in ("Button", "SplitButton"):
            for b in self.mp.descendants(control_type=ct):
                try:
                    if b.window_text().strip() == name:
                        b.invoke()
                        time.sleep(1.4)
                        return True
                except Exception:
                    pass
        return False

    def ribbon_check(self, name, want=False):
        for c in self.mp.descendants(control_type="CheckBox"):
            try:
                if c.window_text().strip() == name:
                    if bool(c.get_toggle_state()) != want:
                        c.toggle()
                        time.sleep(1.2)
                    return True
            except Exception:
                pass
        return False

    # ---------------- выбор задачи
    def select_task(self, fragment, task_id):
        for d in self.mp.descendants(control_type="DataItem"):
            try:
                if fragment.lower() in d.window_text().lower():
                    d.select()
                    time.sleep(0.9)
                    return True
            except Exception:
                continue
        self.show()
        try:
            user32.SetForegroundWindow(self.hwnd)
        except Exception:
            pass
        time.sleep(0.4)
        if not keys_to_pid("{HOME}", self.pid):
            say("   клавиатура недоступна (в фокусе чужое окно) - выбор строки пропущен")
            return False
        time.sleep(0.5)
        for _ in range(task_id - 1):
            if not keys_to_pid("{DOWN}", self.pid):
                break
        time.sleep(1.0)
        return True

    def wait_ready(self, timeout=40):
        """Ждёт, пока приложение перестанет быть «занятым»."""
        t0 = time.time()
        while time.time() - t0 < timeout:
            try:
                self.app.ActiveProject.Tasks.Count
                return True
            except Exception:
                time.sleep(0.8)
        return False

    # ---------------- диалог
    def wait_dialog(self, timeout=20):
        """Ищет НОВЫЙ диалог процесса MS Project и сразу уводит его за экран."""
        t0 = time.time()
        while time.time() - t0 < timeout:
            for h, cls, title in windows():
                if h in self.pre or cls == MAIN_CLASS or cls in SKIP_CLASSES:
                    continue
                if pid_of(h) != self.pid:          # только окна нашего MS Project
                    continue
                if not title:
                    continue
                l, t, r, b = rect(h)
                if (r - l) < 200 or (b - t) < 120:
                    continue
                move_off(h)
                time.sleep(0.7)
                return h, title
            time.sleep(0.03)
        return None, None

    def dlg_ui(self, hwnd):
        try:
            return self.dsk.window(handle=hwnd)
        except Exception:
            return None

    def dlg_tab(self, hwnd, name):
        """Выбирает вкладку/пункт списка диалога (по имени), без мыши."""
        d = self.dlg_ui(hwnd)
        if d is None:
            return False
        for ct in ("TabItem", "ListItem", "Button", "Text"):
            try:
                for t in d.descendants(control_type=ct):
                    nm = t.window_text().strip()
                    if nm == name or nm.startswith(name):
                        try:
                            t.select()
                        except Exception:
                            t.click_input()
                        time.sleep(1.4)
                        return True
            except Exception as e:
                say("   dlg_tab[%s]: %s" % (ct, str(e)[:60]))
        return False

    def dlg_button(self, hwnd, name):
        """Нажимает кнопку диалога (имя может быть с хвостом, напр. «Далее >»)."""
        d = self.dlg_ui(hwnd)
        if d is not None:
            try:
                for b in d.descendants(control_type="Button"):
                    nm = b.window_text().strip()
                    if nm == name or nm.startswith(name):
                        b.invoke()
                        time.sleep(1.6)
                        return True
            except Exception as e:
                say("   dlg_button:", str(e)[:70])
        return False

    def dlg_has_text(self, hwnd, text):
        """Есть ли в диалоге элемент с указанным текстом."""
        d = self.dlg_ui(hwnd)
        if d is None:
            return False
        try:
            for e in d.descendants():
                try:
                    if text.lower() in e.window_text().lower():
                        return True
                except Exception:
                    continue
        except Exception:
            return False
        return False

    def dlg_click_text(self, hwnd, text):
        """Щелчок по элементу диалога с указанным текстом (диалог на экране на 1 с)."""
        l, t, r, b = rect(hwnd)
        user32.SetWindowPos(hwnd, 0, 0, 0, r - l, b - t, 0x0040)
        time.sleep(1.0)
        d = self.dlg_ui(hwnd)
        ok = False
        if d is not None:
            try:
                for e in d.descendants():
                    try:
                        if e.window_text().strip() == text:
                            say("   щелчок по «%s»" % text)
                            e.click_input()
                            ok = True
                            break
                    except Exception:
                        continue
            except Exception as ex:
                say("   dlg_click_text:", str(ex)[:70])
        time.sleep(1.5)
        move_off(hwnd)
        time.sleep(0.6)
        return ok

    def dlg_button_enabled(self, hwnd, name):
        """Проверяет, активна ли кнопка диалога (признак перехода на следующую страницу)."""
        d = self.dlg_ui(hwnd)
        if d is None:
            return None
        try:
            for b in d.descendants(control_type="Button"):
                if b.window_text().strip().startswith(name):
                    return bool(b.is_enabled())
        except Exception:
            return None
        return None

    def close_all(self):
        """Закрывает ТОЛЬКО диалоговые окна MS Project (по PID).

        Никогда не отправляет WM_CLOSE посторонним окнам: рабочему столу,
        панели задач, оболочке explorer.exe и приложениям пользователя.
        """
        for h, cls, _ in windows():
            if cls in FORBIDDEN_CLASSES or cls == MAIN_CLASS:
                continue
            if pid_of(h) != self.pid:            # только процесс MS Project
                continue
            try:
                user32.PostMessageW(h, 0x0010, 0, 0)   # WM_CLOSE
            except Exception:
                pass
        time.sleep(0.8)
        self.esc_to_mp()

    def esc_to_mp(self):
        """Отправляет ESC только если на переднем плане именно MS Project."""
        return keys_to_pid("{ESC}", self.pid)


def shot_notes(s):
    s.select_task("офлайн-режима", 29)
    s.menu("Проект", "Сведения о задаче...")
    h, title = s.wait_dialog()
    if not h:
        raise RuntimeError("диалог не найден")
    say("вкладка Заметки:", s.dlg_click_text(h, "Заметки"))
    return capture(h, os.path.join(paths.SHOTS, "03_заметки_задачи.png"))


def shot_wizard(s):
    s.menu("Формат", "Мастер диаграмм Ганта...")
    h, title = s.wait_dialog()
    if not h:
        raise RuntimeError("диалог не найден")
    # мастер переводится на второй шаг реальным щелчком мыши по «Далее >»
    l, t, r, b = rect(h)
    user32.SetWindowPos(h, 0, 0, 0, r - l, b - t, 0x0040)
    time.sleep(1.2)
    d = s.dlg_ui(h)          # UIA заново: иначе координаты устаревшие
    clicked = False
    if d is not None:
        try:
            for btn in d.descendants(control_type="Button"):
                if btn.window_text().strip().startswith("Далее"):
                    say("   клик по «Далее»")
                    btn.click_input()
                    clicked = True
                    break
        except Exception as e:
            say("   click:", str(e)[:70])
    say("   щелчок выполнен:", clicked)
    time.sleep(1.8)
    move_off(h)
    time.sleep(0.8)
    return capture(h, os.path.join(paths.SHOTS, "13_мастер_диаграмм_ганта.png"))


def shot_options(s):
    s.menu("Сервис", "Параметры...")
    h, title = s.wait_dialog()
    if not h:
        raise RuntimeError("диалог не найден")
    say("раздел Расписание:", s.dlg_tab(h, "Расписание"))
    return capture(h, os.path.join(paths.SHOTS, "21_параметры.png"))


def shot_tab(s, name, tab):
    steps = [("Вид", lambda: s.ribbon_tab("Вид")),
             ("Гант", lambda: s.ribbon_button("Диаграмма Ганта")),
             ("шкала", lambda: s.ribbon_check("Временная шкала", want=False)),
             ("весь проект", lambda: s.ribbon_button("Весь проект")),
             ("вкладка", lambda: s.ribbon_tab(tab))]
    for attempt in range(4):
        try:
            s.wait_ready()
            s.hide()
            time.sleep(0.5)
            for label, fn in steps:
                fn()
                say("   %s: %s" % (name, label))
            time.sleep(1.4)
            return capture(s.hwnd, os.path.join(paths.SHOTS, name + ".png"))
        except Exception as e:
            say("   %s retry %d: %s" % (name, attempt, str(e)[:70]))
            time.sleep(4.0)
            s.refresh()
    raise RuntimeError("не удалось снять " + name)


TASKS = {
    "03": lambda s: shot_notes(s),
    "13": lambda s: shot_wizard(s),
    "21": lambda s: shot_options(s),
    "33": lambda s: shot_tab(s, "33_вкладка_задача", "Задача"),
    "34": lambda s: shot_tab(s, "34_вкладка_ресурс", "Ресурс"),
    "35": lambda s: shot_tab(s, "35_вкладка_проект", "Проект"),
    "36": lambda s: shot_tab(s, "36_вкладка_отчет", "Отчет"),
}


def main():
    which = sys.argv[1]
    s = Shot()
    try:
        size = TASKS[which](s)
        say("OK %s -> %s" % (which, size))
    except Exception as e:
        say("FAIL %s: %s" % (which, str(e)[:160]))
    finally:
        try:
            s.close_all()
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
