"""
Съёмка скриншотов из MS Project для отчёта по практическим работам.
Меню и лента активируются через UIA-паттерн Invoke, диалоги ищутся через Win32.
"""
import ctypes
import os
import sys
import time
import traceback
from ctypes import wintypes

import win32com.client as w
from PIL import ImageGrab
from pywinauto import Desktop
from pywinauto.keyboard import send_keys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from winfocus import keys_to_pid

OUT = paths.SHOTS
MPP = paths.MPP
LOG = os.path.join(paths.BUILD, "shots_log.txt")

user32 = ctypes.windll.user32
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)

log_fh = open(LOG, "w", encoding="utf-8", buffering=1)


def L(msg):
    log_fh.write(str(msg) + "\n")
    print(msg, flush=True)


def get_rect(hwnd):
    r = wintypes.RECT()
    user32.GetWindowRect(wintypes.HWND(hwnd), ctypes.byref(r))
    return (r.left, r.top, r.right, r.bottom)


def pid_of(hwnd):
    p = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
    return p.value


class Shooter(object):
    def __init__(self):
        self.app = w.Dispatch("MSProject.Application")
        self.app.Visible = True
        self.app.DisplayAlerts = 0
        self.done = []
        self.failed = []
        self.mp = None
        self.mb = None
        # открываем файл и ждём готовности окна (до 60 с)
        t0 = time.time()
        opened = False
        while time.time() - t0 < 60:
            try:
                self.app.FileOpen(MPP)
                opened = True
                break
            except Exception as e:
                L("  ! FileOpen: %s" % str(e)[:70])
                time.sleep(3)
        if not opened:
            raise RuntimeError("не удалось открыть файл проекта")
        while time.time() - t0 < 60:
            try:
                cands = [x for x in self.dsk_windows()
                         if x.class_name() == "JWinproj-WhimperMainClass"]
                for c in cands:
                    r = c.rectangle()
                    if (r.right - r.left) > 500 and (r.bottom - r.top) > 300:
                        self.mp = c
                        break
                if self.mp is not None:
                    mbs = [m for m in self.mp.descendants(control_type="MenuBar")
                           if "меню" in m.window_text()]
                    if mbs:
                        self.mb = mbs[0]
                        break
            except Exception:
                pass
            time.sleep(2)
        if self.mp is None or self.mb is None:
            raise RuntimeError("окно MS Project не готово")
        self.mp.set_focus()
        try:
            self.mp.maximize()
        except Exception:
            pass
        time.sleep(2.5)
        self.mp_hwnd = self.mp.handle
        self.pid = pid_of(self.mp_hwnd)
        L("окно готово: %s" % self.mp.window_text()[:60])

    def dsk_windows(self):
        return Desktop(backend="uia").windows()

    # ---------- Win32-поиск окон процесса
    def proc_windows(self):
        res = []

        def cb(h, l):
            if pid_of(h) == self.pid and bool(user32.IsWindowVisible(h)):
                cls = ctypes.create_unicode_buffer(256)
                user32.GetClassNameW(h, cls, 256)
                ti = ctypes.create_unicode_buffer(512)
                user32.GetWindowTextW(h, ti, 512)
                res.append((h, cls.value, ti.value))
            return True

        user32.EnumWindows(EnumWindowsProc(cb), 0)
        return res

    def find_dialog(self, before_handles, timeout=22):
        t0 = time.time()
        while time.time() - t0 < timeout:
            for h, cls, title in self.proc_windows():
                if h in before_handles:
                    continue
                if cls in ("JWinproj-WhimperMainClass", "#32768", "SysShadow"):
                    continue
                if "Ожидание подключения принтера" in title:
                    continue
                l, t, r, b = get_rect(h)
                if (r - l) < 380 or (b - t) < 240:
                    continue
                return h, cls, title
            time.sleep(0.4)
        return None

    def find_popup_menu(self, timeout=6):
        t0 = time.time()
        while time.time() - t0 < timeout:
            for h, cls, title in self.proc_windows():
                if cls == "#32768":
                    return h
            time.sleep(0.3)
        return None

    # ---------- захват
    def grab_hwnd(self, hwnd, path):
        l, t, r, b = get_rect(hwnd)
        sw, sh = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        l, t = max(0, l), max(0, t)
        r, b = min(sw, r), min(sh, b)
        if r <= l or b <= t:
            raise RuntimeError("пустой прямоугольник")
        img = ImageGrab.grab(bbox=(l, t, r, b))
        img.save(path)
        return img.size

    def grab_window(self, path):
        return self.grab_hwnd(self.mp_hwnd, path)

    # ---------- UIA helpers
    def uia_win(self, hwnd):
        for x in self.dsk_windows():
            try:
                if x.handle == hwnd:
                    return x
            except Exception:
                pass
        return None

    def act(self, element):
        """Активирует элемент: сначала Invoke, при отказе - клик."""
        try:
            element.invoke()
            return True
        except Exception:
            pass
        try:
            element.click_input()
            return True
        except Exception as e:
            L("  ! act: %s" % str(e)[:80])
            return False

    def refresh_mp(self):
        """Перезапрашивает UIA-объект главного окна (после смены представления он устаревает)."""
        try:
            cands = [x for x in self.dsk_windows()
                     if x.class_name() == "JWinproj-WhimperMainClass"]
            for c in cands:
                r = c.rectangle()
                if (r.right - r.left) > 500 and (r.bottom - r.top) > 300:
                    self.mp = c
                    return True
        except Exception:
            pass
        return False

    # ---------- меню
    def get_menu(self):
        """Перечитывает строку меню (элемент может устареть)."""
        for attempt in range(2):
            try:
                for m in self.mp.descendants(control_type="MenuBar"):
                    if "меню" in m.window_text():
                        return m
            except Exception:
                pass
            self.refresh_mp()
            time.sleep(0.5)
        return None

    def focus_main(self):
        try:
            user32.SetForegroundWindow(self.mp_hwnd)
        except Exception:
            pass
        try:
            self.mp.set_focus()
        except Exception:
            pass

    def menu(self, *path):
        last = ""
        for attempt in range(4):
            try:
                keys_to_pid("{ESC}", self.pid)
                time.sleep(0.5)
                try:
                    user32.SetForegroundWindow(self.mp_hwnd)
                except Exception:
                    pass
                self.refresh_mp()
                time.sleep(0.6)
                mb = self.get_menu()
                if mb is None:
                    last = "нет строки меню"
                    time.sleep(1.0)
                    continue
                top = None
                for t in mb.children():
                    if t.window_text().strip() == path[0]:
                        top = t
                        break
                if top is None:
                    last = "нет меню " + path[0]
                    time.sleep(1.0)
                    continue
                self.act(top)
                time.sleep(1.0)
                cur = top
                for label in path[1:]:
                    found = None
                    for k in cur.children():
                        if k.window_text().strip().strip("[]").startswith(label):
                            found = k
                            break
                    if found is None:
                        last = "нет пункта " + label
                        raise RuntimeError(last)
                    self.act(found)
                    time.sleep(1.1)
                    cur = found
                time.sleep(1.2)
                return True
            except Exception as e:
                last = str(e)[:90]
                try:
                    keys_to_pid("{ESC}{ESC}", self.pid)
                except Exception:
                    pass
                time.sleep(1.2)
        L("  ! меню %s: %s" % ("/".join(path), last))
        try:
            keys_to_pid("{ESC}{ESC}", self.pid)
        except Exception:
            pass
        return False

    def popup_item_cmd(self, popup_hwnd, text):
        """Ищет пункт во всплывающем меню (#32768) и возвращает его команду."""
        hmenu = user32.GetMenu(wintypes.HWND(popup_hwnd))
        if not hmenu:
            return None
        count = user32.GetMenuItemCount(hmenu)
        for i in range(count):
            buf = ctypes.create_unicode_buffer(512)
            user32.GetMenuStringW(hmenu, i, buf, 512, 0x400)  # MF_BYPOSITION
            if buf.value.replace("&", "").strip() == text:
                return user32.GetMenuItemID(hmenu, i)
        return None

    def menu_dynamic(self, top_label, sub_prefix, item_label):
        """Вид -> [Представления задач] -> Диаграмма Ганта (динамическое меню)."""
        try:
            mb = self.get_menu()
            top = [t for t in mb.children()
                   if t.window_text().strip() == top_label][0]
            self.act(top)
            time.sleep(0.9)
            sub = [k for k in top.children()
                   if k.window_text().strip().strip("[]").startswith(sub_prefix)][0]
            self.act(sub)
            time.sleep(1.6)
            h = self.find_popup_menu()
            if h:
                cmd = self.popup_item_cmd(h, item_label)
                if cmd is not None:
                    user32.PostMessageW(self.mp_hwnd, 0x0111, cmd, 0)
                    time.sleep(1.6)
                    return True
                pw = self.uia_win(h)
                if pw:
                    for it in pw.descendants(control_type="MenuItem"):
                        if it.window_text().strip() == item_label:
                            self.act(it)
                            time.sleep(1.5)
                            return True
            # ищем пункт среди всех MenuItem окна (выпадающие списки ленты)
            try:
                for it in self.mp.descendants(control_type="MenuItem"):
                    if it.window_text().strip() == item_label:
                        self.act(it)
                        time.sleep(1.5)
                        return True
            except Exception:
                pass
            for k in sub.children():
                if k.window_text().strip() == item_label:
                    self.act(k)
                    time.sleep(1.5)
                    return True
            raise RuntimeError("не найден пункт " + item_label)
        except Exception as e:
            L("  ! меню %s/%s/%s: %s" % (top_label, sub_prefix, item_label, str(e)[:90]))
            try:
                keys_to_pid("{ESC}{ESC}", self.pid)
            except Exception:
                pass
            return False

    # ---------- лента
    def ribbon_tab(self, name):
        for attempt in range(3):
            try:
                try:
                    self.mp.set_focus()
                except Exception:
                    pass
                self.refresh_mp()
                t = [x for x in self.mp.descendants(control_type="TabItem")
                     if x.window_text().strip() == name][0]
                t.click_input()
                time.sleep(1.3)
                return True
            except Exception as e:
                L("  ! лента[%s]: %s" % (name, str(e)[:70]))
                time.sleep(1.0)
        return False

    def ribbon_click(self, button):
        """Ищет кнопку ленты по имени и активирует её (лента не поддерживает Invoke)."""
        for attempt in range(3):
            for ct in ("Button", "SplitButton", "MenuItem", "CheckBox"):
                try:
                    cands = [b for b in self.mp.descendants(control_type=ct)
                             if b.window_text().strip() == button]
                except Exception:
                    continue
                if not cands:
                    continue
                for b in cands:
                    try:
                        b.click_input()
                        time.sleep(1.5)
                        return True
                    except Exception:
                        continue
            # возможно, активна другая вкладка - переключаемся на «Вид»
            try:
                self.ribbon_tab("Вид")
                time.sleep(0.8)
            except Exception:
                pass
        raise RuntimeError("не найдена кнопка: " + button)

    def ribbon_dropdown(self, button, item):
        """Открывает раскрывающийся список кнопки ленты и выбирает пункт."""
        self.ribbon_tab("Вид")
        target = None
        for ct in ("SplitButton", "Button"):
            for b in self.mp.descendants(control_type=ct):
                try:
                    if b.window_text().strip() == button:
                        target = b
                        break
                except Exception:
                    pass
            if target:
                break
        if target is None:
            raise RuntimeError("нет кнопки " + button)
        for sub in target.descendants():
            try:
                if sub.element_info.control_type in ("ComboBox", "Button", "Menu"):
                    sub.click_input()
                    time.sleep(1.2)
                    break
            except Exception:
                continue
        else:
            target.click_input()
            time.sleep(1.2)
        for it in self.mp.descendants(control_type="MenuItem"):
            try:
                if it.window_text().strip() == item:
                    it.click_input()
                    time.sleep(1.5)
                    return True
            except Exception:
                continue
        raise RuntimeError("нет пункта " + item)

    # ---------- выбор строки таблицы
    def select_row(self, fragment):
        try:
            keys_to_pid("{HOME}", self.pid)
            time.sleep(0.5)
            for d in self.mp.descendants(control_type="DataItem"):
                try:
                    if fragment.lower() in d.window_text().lower():
                        d.click_input()
                        time.sleep(0.9)
                        return True
                except Exception:
                    continue
            raise RuntimeError("строка не найдена: " + fragment)
        except Exception as e:
            L("  ! выбор строки[%s]: %s" % (fragment, str(e)[:70]))
            return False

    def select_task_id(self, tid):
        """Выбор задачи по порядковому номеру в списке (Home + Down)."""
        try:
            self.mp.set_focus()
            time.sleep(0.4)
            keys_to_pid("{HOME}", self.pid)
            time.sleep(0.5)
            for _ in range(tid - 1):
                keys_to_pid("{DOWN}", self.pid)
            time.sleep(0.9)
            return True
        except Exception as e:
            L("  ! выбор задачи #%s: %s" % (tid, str(e)[:70]))
            return False

    # ---------- снимки
    def shot_dialog(self, name, menu_path, select=None, select_id=None):
        path = os.path.join(OUT, name + ".png")
        try:
            if select_id:
                self.select_task_id(select_id)
            elif select:
                self.select_row(select)
            before = set(h for h, c, t in self.proc_windows())
            if not self.menu(*menu_path):
                raise RuntimeError("меню не открыто")
            d = self.find_dialog(before)
            if d is None:
                raise RuntimeError("диалог не найден")
            time.sleep(1.2)
            size = self.grab_hwnd(d[0], path)
            L("OK   %-38s %s  %r" % (name, size, d[2][:42]))
            self.done.append(name)
            keys_to_pid("{ESC}", self.pid)
            time.sleep(0.8)
            keys_to_pid("{ESC}", self.pid)
            time.sleep(0.5)
        except Exception as e:
            L("FAIL %-38s %s" % (name, str(e)[:110]))
            self.failed.append(name)
            try:
                keys_to_pid("{ESC}{ESC}", self.pid)
            except Exception:
                pass
            time.sleep(0.6)

    def fit_whole(self):
        """Масштаб «Весь проект» + отключение временной шкалы."""
        try:
            for c in self.mp.descendants(control_type="CheckBox"):
                try:
                    if c.window_text().strip() == "Временная шкала" and c.get_toggle_state():
                        c.click_input()
                        time.sleep(1.4)
                        break
                except Exception:
                    continue
        except Exception:
            pass
        try:
            self.ribbon_click("Весь проект")
        except Exception:
            pass

    def shot_view(self, name, view_name):
        path = os.path.join(OUT, name + ".png")
        ok = False
        try:
            self.ribbon_tab("Вид")
            self.ribbon_click(view_name)
            ok = True
        except Exception as e:
            L("  ! лента: %s -> %s" % (view_name, str(e)[:60]))
        if not ok:
            try:
                if not self.menu_dynamic("Вид", "Представления", view_name):
                    raise RuntimeError("представление не выбрано")
            except Exception as e:
                L("FAIL %-38s %s" % (name, str(e)[:110]))
                self.failed.append(name)
                return
        try:
            time.sleep(0.8)
            self.fit_whole()
            time.sleep(0.8)
            size = self.grab_window(path)
            L("OK   %-38s %s (%s)" % (name, size, view_name))
            self.done.append(name)
        except Exception as e:
            L("FAIL %-38s %s" % (name, str(e)[:110]))
            self.failed.append(name)

    def shot_tab(self, name, tab):
        path = os.path.join(OUT, name + ".png")
        try:
            self.ribbon_tab(tab)
            time.sleep(1.2)
            size = self.grab_window(path)
            L("OK   %-38s %s (%s)" % (name, size, tab))
            self.done.append(name)
        except Exception as e:
            L("FAIL %-38s %s" % (name, str(e)[:110]))
            self.failed.append(name)

    def shot_ribbon(self, name, tab, button):
        path = os.path.join(OUT, name + ".png")
        try:
            self.ribbon_tab(tab)
            self.ribbon_click(button)
            time.sleep(1.0)
            size = self.grab_window(path)
            L("OK   %-38s %s (%s/%s)" % (name, size, tab, button))
            self.done.append(name)
        except Exception as e:
            L("FAIL %-38s %s" % (name, str(e)[:110]))
            self.failed.append(name)

    # ---------- сценарий
    def run(self):
        # --- представления (до диалогов: они оставляют приложение в рабочем состоянии)
        self.shot_view("26_диаграмма_ганта", "Диаграмма Ганта")
        self.shot_view("27_использование_задач", "Использование задач")
        self.shot_view("28_сетевой_график", "Сетевой график")
        self.shot_view("29_календарь", "Календарь")
        self.shot_view("30_лист_ресурсов", "Лист ресурсов")
        self.shot_view("31_использование_ресурсов", "Использование ресурсов")
        try:
            self.ribbon_dropdown("Использование ресурсов", "Диаграмма использования ресурсов")
            time.sleep(1.2)
            size = self.grab_window(os.path.join(OUT, "32_диаграмма_использования_ресурсов.png"))
            L("OK   %-38s %s (ресурсная диаграмма)" % ("32_диаграмма_использования_ресурсов", size))
            self.done.append("32")
        except Exception as e:
            L("FAIL %-38s %s" % ("32_диаграмма_использования_ресурсов", str(e)[:100]))
            self.failed.append("32")

        # --- возвращаемся к диаграмме Ганта (состав меню зависит от представления)
        try:
            self.ribbon_tab("Вид")
            self.ribbon_click("Диаграмма Ганта")
            time.sleep(1.2)
        except Exception:
            pass

        # --- диалоги
        self.shot_dialog("01_сведения_о_проекте", ("Проект", "Сведения о проекте..."))
        self.shot_dialog("02_сведения_о_задаче", ("Проект", "Сведения о задаче..."),
                         select_id=39)
        self.shot_dialog("03_заметки_задачи", ("Проект", "Заметки задачи..."),
                         select_id=62)
        self.shot_dialog("04_изменить_рабочее_время", ("Сервис", "Изменить рабочее время..."))
        self.shot_dialog("05_выравнивание_ресурсов", ("Сервис", "Выравнивание загрузки ресурсов..."))
        self.shot_dialog("06_назначить_ресурсы", ("Сервис", "Назначить ресурсы..."),
                         select_id=344)
        self.shot_dialog("07_вставить_столбец", ("Вставка", "Столбец..."), select_id=34)
        self.shot_dialog("08_сортировка", ("Проект", "Сортировка", "Сортировать по..."))
        self.shot_dialog("09_другие_фильтры", ("Проект", "Фильтр", "Другие фильтры..."))
        self.shot_dialog("10_задать_базовый_план",
                         ("Сервис", "Отслеживание", "Задать базовый план..."))
        self.shot_dialog("11_обновить_задачи", ("Сервис", "Отслеживание", "Обновить задачи..."))
        self.shot_dialog("13_мастер_диаграмм_ганта", ("Формат", "Мастер диаграмм Ганта..."))
        self.shot_dialog("14_стили_отрезков", ("Формат", "Стили отрезков..."))
        self.shot_dialog("15_стили_текста", ("Формат", "Стили текста..."))
        self.shot_dialog("16_масштаб", ("Вид", "Масштаб..."))
        self.shot_dialog("17_отчеты", ("Отчет", "Отчеты..."))
        self.shot_dialog("18_наглядные_отчеты", ("Отчет", "Наглядные отчеты..."))
        self.shot_dialog("19_повторяющаяся_задача", ("Вставка", "Повторяющаяся задача..."))
        self.shot_dialog("20_гиперссылка", ("Вставка", "Гиперссылка..."), select_id=345)
        self.shot_dialog("21_параметры", ("Сервис", "Параметры..."))
        self.shot_dialog("22_формат_отрезка", ("Формат", "Формат отрезка..."))
        self.shot_dialog("23_найти", ("Правка", "Найти..."))
        self.shot_dialog("24_связи_задач", ("Правка", "Связи..."))

        # --- вкладки ленты
        self.shot_tab("33_вкладка_задача", "Задача")
        self.shot_tab("34_вкладка_ресурс", "Ресурс")
        self.shot_tab("35_вкладка_проект", "Проект")
        self.shot_tab("36_вкладка_отчет", "Отчет")

        # --- параметры страницы (в конце: вызывает ожидание принтера)
        self.shot_dialog("12_параметры_страницы", ("Файл", "Параметры страницы..."))


if __name__ == "__main__":
    s = Shooter()
    try:
        s.run()
    except Exception:
        traceback.print_exc()
    L("---- ГОТОВО: успешно %d, ошибок %d" % (len(s.done), len(s.failed)))
    L("ошибки: %s" % s.failed)
