"""Поиск периодов реальной перегрузки по шкале времени."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say

NAMES = ("Бизнес-аналитик", "Бэкенд-разработчик", "DevOps-инженер",
         "Тестировщик")


def main():
    s = Shot()
    try:
        p = s.app.ActiveProject
        start, finish = p.ProjectStart, p.ProjectFinish
        for r in p.Resources:
            if r.Name not in NAMES:
                continue
            say("=== %s Max=%.2f Over=%s" % (r.Name, r.MaxUnits, r.Overallocated))
            for typ, label in ((3, "peak"), (5, "avail")):
                try:
                    vals = r.TimeScaleData(start, finish, typ, 2)
                    bad = []
                    for i in range(1, vals.Count + 1):
                        v = vals(i).Value
                        d0 = str(vals(i).Start)[:10]
                        if label == "peak" and v > r.MaxUnits + 0.001:
                            bad.append((d0, v))
                    say("  %s: точек %d, превышений %d %s"
                        % (label, vals.Count, len(bad),
                           bad[:8]))
                except Exception as e:
                    say("  %s ERR %s" % (label, str(e)[:100]))
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
