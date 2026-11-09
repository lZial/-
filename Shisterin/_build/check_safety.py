"""
Проверка безопасности: кому вообще мог бы уйти WM_CLOSE из скриптов.
Ничего не отправляет и не закрывает - только перечисление.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from winfocus import (FORBIDDEN_CLASSES, pid_of, select_windows_to_close,
                       visible_windows)

print("=" * 72)
print("ВИДИМЫЕ ОКНА ВЕРХНЕГО УРОВНЯ (окно | класс | PID | заголовок)")
print("=" * 72)
rows = []
for h, cls in visible_windows():
    import ctypes
    from ctypes import wintypes
    ti = ctypes.create_unicode_buffer(512)
    ctypes.windll.user32.GetWindowTextW(h, ti, 512)
    rows.append((pid_of(h), cls, ti.value, h))
for pid, cls, title, h in sorted(rows, key=lambda r: (r[0], r[1])):
    print("  pid=%-6s %-32s %s" % (pid, cls[:32], title[:44]))

print()
print("=" * 72)
print("ПРОВЕРКА close_all(): отбор окон для WM_CLOSE")
print("=" * 72)
# имитируем PID приложения MS Project: берём все PID, где есть окно MS Project
mp_pids = set(pid for pid, cls, t, h in rows if cls.startswith("JWinproj"))
print("PID процессов MS Project, найденных в списке:", mp_pids or "нет запущенных")
for pid in sorted(mp_pids) or [0]:
    targets = select_windows_to_close(pid)
    print()
    print("  PID %s -> к закрытию допущено %d окон:" % (pid, len(targets)))
    for h, cls in targets:
        title = ""
        for p2, c2, t2, h2 in rows:
            if h2 == h:
                title = t2
        print("      %-32s %s" % (cls[:32], title[:44]))

print()
print("=" * 72)
print("КОНТРОЛЬНЫЙ СПИСОК: чужие приложения не должны попасть в отбор")
print("=" * 72)
all_pids = set(pid for pid, cls, t, h in rows)
for pid in sorted(all_pids):
    targets = select_windows_to_close(pid)
    names = []
    for h, cls in targets:
        for p2, c2, t2, h2 in rows:
            if h2 == h and t2:
                names.append(t2)
    print("  pid=%-6s допущено к закрытию: %s" % (pid, "; ".join(n[:38] for n in names) or "-"))

print()
print("ЗАПРЕЩЁННЫЕ КЛАССЫ (не закрываются никогда):")
print("   " + ", ".join(FORBIDDEN_CLASSES))
bad = [c for pid, cls, t, h in rows
       if cls in FORBIDDEN_CLASSES and any(h2 == h for h2, _ in select_windows_to_close(pid))]
print()
print("ОКОН ЗАПРЕЩЁННЫХ КЛАССОВ, ПОПАВШИХ В ОТБОР:", bad if bad else "нет - корректно")

# Главный инвариант: при любом PID в отбор попадают только окна этого PID.
print()
print("=" * 72)
print("ИНВАРИАНТ: в отбор для PID попадают только окна этого PID")
print("=" * 72)
ok = True
for pid in sorted(all_pids):
    targets = select_windows_to_close(pid)
    foreign = [h for h, c in targets if pid_of(h) != pid]
    if foreign:
        ok = False
    print("  pid=%-6s отобрано %d, чужих PID среди них: %d" % (pid, len(targets), len(foreign)))
print()
print("ИНВАРИАНТ ВЫПОЛНЕН:", "да" if ok else "НЕТ - ОШИБКА")
print("=" * 72)
