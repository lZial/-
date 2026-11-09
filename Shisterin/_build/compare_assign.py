"""Сравнение назначений и разбиений старого и нового файлов."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say

OLD = os.path.join(paths.BUILD, "backup_2026_fixed.mpp")
NEW = os.path.join(paths.BASE, "УП_Шистерин.mpp")
NAMES = ("Бизнес-аналитик", "DevOps-инженер", "Бэкенд-разработчик",
         "Тестировщик")


def dump(app, tag):
    p = app.ActiveProject
    say("=====", tag)
    for r in p.Resources:
        if r.Name not in NAMES:
            continue
        say("--", r.Name, "Over=", r.Overallocated)
        for a in r.Assignments:
            t = None
            for x in p.Tasks:
                if x.ID == a.TaskID:
                    t = x
                    break
            parts = t.SplitParts.Count if t is not None else "?"
            say("   T%-4s %s .. %s u=%.0f%% split=%s %s"
                % (a.TaskID, str(a.Start)[:10], str(a.Finish)[:10],
                   a.Units * 100, parts, a.TaskName[:30]))


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
