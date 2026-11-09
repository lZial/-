"""
Безопасная работа с клавиатурой и окнами.

Правила безопасности:
  * клавиши отправляются ТОЛЬКО в то окно, которое сейчас на переднем плане
    И принадлежит нужному процессу (иначе они уйдут в приложение пользователя);
  * класс окна проверяется по запретному списку: рабочий стол, панель задач,
    оболочку explorer.exe и окна UWP-приложений не трогаем никогда;
  * WM_CLOSE отправляется только окнам конкретного процесса.
"""
import ctypes
from ctypes import wintypes

from pywinauto.keyboard import send_keys

user32 = ctypes.windll.user32

# Окна, которые запрещено трогать никогда
FORBIDDEN_CLASSES = (
    # оболочка Windows и рабочий стол
    "Progman", "WorkerW", "Shell_TrayWnd", "SHELLDLL_DefView", "SysListView32",
    "DummyDWMListenerWindow", "EdgeUiInputTopWndClass", "DV2ControlHost",
    "SysPager", "Button", "CicMarshalWnd",
    # окна UWP-приложений и служебные
    "ApplicationFrameWindow", "Windows.UI.Core.CoreWindow", "NotifyIconOverflowWindow",
    "Windows.UI.Composition.DesktopWindowContentBridge", "Xaml_WindowedPopupClass",
    "tooltips_class32", "SysShadow", "MSO_BORDEREFFECT_WINDOW_CLASS",
    "IME", "MSCTFIME UI", "Default IME",
)


def pid_of(hwnd):
    """Идентификатор процесса по дескриптору окна."""
    p = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
    return p.value


def foreground_pid():
    """PID процесса окна на переднем плане (0 - окна нет)."""
    fg = user32.GetForegroundWindow()
    return pid_of(fg) if fg else 0


def class_of(hwnd):
    cls = ctypes.create_unicode_buffer(256)
    user32.GetClassNameW(hwnd, cls, 256)
    return cls.value


def keys_to_pid(keys, pid):
    """Отправляет клавиши, только если активное окно принадлежит процессу pid.

    Возвращает True, если клавиши отправлены, иначе False (окно чужое - не трогаем).
    """
    try:
        fg = user32.GetForegroundWindow()
        if not fg:
            return False
        if pid_of(fg) != pid:
            return False
        if class_of(fg) in FORBIDDEN_CLASSES:
            return False
        send_keys(keys)
        return True
    except Exception:
        return False


def select_windows_to_close(pid, skip_classes=(), extra_skip=()):
    """Отбирает окна процесса pid, которым разрешено отправить WM_CLOSE.

    Возвращает список (hwnd, класс). Ничего не отправляет - только отбор,
    поэтому функцию безопасно вызывать для проверки.
    """
    skip = set(FORBIDDEN_CLASSES) | set(skip_classes) | set(extra_skip)
    targets = []
    for h, cls in visible_windows():
        if cls in skip:
            continue
        if pid_of(h) != pid:
            continue
        targets.append((h, cls))
    return targets


def close_windows_of(pid, skip_classes=(), extra_skip=()):
    """Закрывает (WM_CLOSE) только видимые окна указанного процесса.

    Окна из FORBIDDEN_CLASSES и skip_classes не затрагиваются.
    """
    closed = []
    for h, cls in select_windows_to_close(pid, skip_classes, extra_skip):
        try:
            user32.PostMessageW(h, 0x0010, 0, 0)   # WM_CLOSE
            closed.append((h, cls))
        except Exception:
            pass
    return closed


def visible_windows():
    """Список (hwnd, класс) видимых окон верхнего уровня."""
    res = []
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)

    def cb(h, l):
        if user32.IsWindowVisible(h):
            res.append((h, class_of(h)))
        return True

    user32.EnumWindows(EnumWindowsProc(cb), 0)
    return res
