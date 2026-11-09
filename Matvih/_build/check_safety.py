"""Проверка безопасности: показывает, каким окнам мог бы уйти WM_CLOSE.

Ничего не закрывает - только перечисляет окна и проверяет, что фильтр
по PID процесса MS Project не захватывает чужие окна.
"""
import ctypes
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from winfocus import (FORBIDDEN_CLASSES, pid_of, select_windows_to_close,
                      visible_windows)

user32 = ctypes.windll.user32


def title_of(hwnd):
    buf = ctypes.create_unicode_buffer(512)
    user32.GetWindowTextW(hwnd, buf, 512)
    return buf.value


def main():
    print("=" * 72)
    print("ВИДИМЫЕ ОКНА (класс | заголовок | PID)")
    print("=" * 72)
    rows = []
    for h, cls in visible_windows():
        rows.append((pid_of(h), cls, title_of(h), h))
    for pid, cls, title, h in sorted(rows, key=lambda r: (r[0], r[1])):
        print("  pid=%-6s %-32s %s" % (pid, cls[:32], title[:44]))

    print()
    print("=" * 72)
    print("ЧТО ЗАКРОЕТ close_all(): только окна процесса MS Project")
    print("=" * 72)
    mp_pids = set(pid for pid, cls, t, h in rows if cls.startswith("JWinproj"))
    print("PID процесса MS Project:", mp_pids or "не найден")
    for pid in sorted(mp_pids) or []:
        targets = select_windows_to_close(pid)
        print("  PID %s -> %d окон:" % (pid, len(targets)))
        for h, cls in targets:
            print("      %-32s %s" % (cls[:32], title_of(h)[:44]))

    print()
    print("=" * 72)
    print("ПРОВЕРКА: фильтр по PID не должен захватывать чужие окна")
    print("=" * 72)
    ok = True
    for pid in sorted(set(r[0] for r in rows)):
        targets = select_windows_to_close(pid)
        foreign = [h for h, c in targets if pid_of(h) != pid]
        if foreign:
            ok = False
        print("  pid=%-6s окон под фильтром: %d, чужих PID: %d"
              % (pid, len(targets), len(foreign)))
    print()
    print("Запретные классы окон:", ", ".join(FORBIDDEN_CLASSES))
    print("Итог:", "OK" if ok else "ОШИБКА - фильтр захватывает чужие окна")
    print("=" * 72)


if __name__ == "__main__":
    main()
