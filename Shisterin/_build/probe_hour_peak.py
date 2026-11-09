"""Почасовой пик загрузки (type=4, hours)."""
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
        a, b = p.ProjectStart, p.ProjectFinish
        t0 = a.replace(minute=0, second=0, microsecond=0)
        for r in p.Resources:
            if r.Type != 0:
                continue
            vals = r.TimeScaleData(a, b, 4, 5, 1)
            peak = 0.0
            when = None
            for i in range(1, vals.Count + 1):
                v = vals(i).Value
                if isinstance(v, (int, float)) and v > peak:
                    peak = v
                    when = t0 + datetime.timedelta(hours=i - 1)
            say("%-28s Max=%.2f  час.пик=%.2f (%s) Over=%s"
                % (r.Name, r.MaxUnits, peak,
                   when.strftime("%d.%m %H:%M") if when else "-",
                   r.Overallocated))
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
