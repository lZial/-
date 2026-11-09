"""Строки доступности проблемных ресурсов."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say

NAMES = ("Бизнес-аналитик", "Бэкенд-разработчик", "DevOps-инженер",
         "Тестировщик")


def fmt(d):
    try:
        return str(d)[:10]
    except Exception:
        return str(d)


def main():
    s = Shot()
    try:
        pr = s.app.ActiveProject
        for r in pr.Resources:
            if r.Name not in NAMES:
                continue
            say("%-28s Max=%.0f%% Peak=%.0f%% Over=%s rows=%d"
                % (r.Name, r.MaxUnits * 100, r.PeakUnits * 100,
                   r.Overallocated, r.Availabilities.Count))
            for i in range(1, r.Availabilities.Count + 1):
                a = r.Availabilities(i)
                say("    %s .. %s : %.0f%%"
                    % (fmt(a.AvailableFrom), fmt(a.AvailableTo),
                       a.AvailableUnit))
        say("--- после пересчёта ---")
        s.app.CalculateProject()
        for r in pr.Resources:
            if r.Name in NAMES:
                say("%-28s Over=%s" % (r.Name, r.Overallocated))
        say("задач перегружено:",
            sum(1 for t in pr.Tasks if t.Overallocated))
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
