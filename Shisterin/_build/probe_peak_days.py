"""Пиковые единицы по дням (type=4, days) и превышения лимита."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say


def main():
    s = Shot()
    try:
        import datetime
        p = s.app.ActiveProject
        a, b = p.ProjectStart, p.ProjectFinish
        d0 = a.date()
        for r in p.Resources:
            if r.Type != 0:
                continue
            vals = r.TimeScaleData(a, b, 4, 4, 1)
            peak = 0.0
            peak_day = None
            over = []
            for i in range(1, vals.Count + 1):
                v = vals(i).Value
                if not isinstance(v, (int, float)):
                    continue
                day = str(d0 + datetime.timedelta(days=i - 1))
                if v > peak:
                    peak, peak_day = v, day
                if v > r.MaxUnits + 0.001:
                    over.append((day, v))
            say("%-28s Max=%.2f Peak=%.2f (%s) Over=%-5s превыш.дней=%d %s"
                % (r.Name, r.MaxUnits, peak, peak_day, r.Overallocated,
                   len(over), over[:4]))
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
