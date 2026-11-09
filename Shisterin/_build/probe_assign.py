"""Назначения проблемных ресурсов с датами."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say

NAMES = ("Бизнес-аналитик", "Бэкенд-разработчик", "DevOps-инженер",
         "Тестировщик")


def d(x):
    try:
        return str(x)[:16]
    except Exception:
        return str(x)


def main():
    s = Shot()
    try:
        p = s.app.ActiveProject
        say("календарь проекта:", p.Calendar.Name)
        for r in p.Resources:
            if r.Name not in NAMES:
                continue
            say("=== %s | Max=%.2f Peak=%.2f Over=%s | календарь=%s"
                % (r.Name, r.MaxUnits, r.PeakUnits, r.Overallocated,
                   getattr(r, "BaseCalendar", "?")))
            rows = []
            for a in r.Assignments:
                rows.append((str(a.Start), str(a.Finish), a.TaskID,
                             a.TaskName[:40], a.Units, a.Work / 60.0))
            for x in sorted(rows):
                say("  %s .. %s | T%-4s %-40s u=%.0f%% w=%.1f"
                    % (x[0][:10], x[1][:10], x[2], x[3], x[4] * 100, x[5]))
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
