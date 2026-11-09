"""Сравнение ресурсов старого и нового файлов."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say

OLD = os.path.join(paths.BUILD, "backup_2026_fixed.mpp")
NEW = os.path.join(paths.BASE, "УП_Шистерин.mpp")
NAMES = ("Бизнес-аналитик", "Бэкенд-разработчик", "DevOps-инженер",
         "Тестировщик")


def dump(app, tag):
    p = app.ActiveProject
    say("=====", tag, "| задач", p.Tasks.Count,
        "| статус", str(p.StatusDate)[:10])
    for r in p.Resources:
        if r.Name not in NAMES:
            continue
        say("%-24s Max=%.2f Peak=%.2f Over=%-5s rows=%d From=%s To=%s"
            % (r.Name, r.MaxUnits, r.PeakUnits, r.Overallocated,
               r.Availabilities.Count,
               str(getattr(r, "AvailableFrom", "?"))[:10],
               str(getattr(r, "AvailableTo", "?"))[:10]))
        for i in range(1, r.Availabilities.Count + 1):
            a = r.Availabilities(i)
            say("      %s .. %s : %.0f"
                % (str(a.AvailableFrom)[:10], str(a.AvailableTo)[:10],
                   a.AvailableUnit))


def main():
    s = Shot()
    try:
        s.app.FileOpen(OLD)
        dump(s.app, "OLD 2026")
        s.app.FileClose(0)
        s.app.FileOpen(NEW)
        dump(s.app, "NEW 2025")
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
