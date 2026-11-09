"""Максимальная суммарная загрузка ресурса по календарным дням."""
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say


def main():
    s = Shot()
    try:
        p = s.app.ActiveProject
        for r in p.Resources:
            if r.Type != 0:
                continue
            days = {}
            for a in r.Assignments:
                try:
                    d0 = a.Start.date()
                    d1 = a.Finish.date()
                except Exception:
                    continue
                u = a.Units
                d = d0
                while d <= d1:
                    days[d] = days.get(d, 0.0) + u
                    d += datetime.timedelta(days=1)
            peak = max(days.values()) if days else 0.0
            day = max(days, key=days.get) if days else None
            flag = "  <-- перегруз" if peak > r.MaxUnits + 0.001 else ""
            say("%-28s Max=%.2f  факт.пик=%.2f (%s)%s"
                % (r.Name, r.MaxUnits, peak, day, flag))
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
