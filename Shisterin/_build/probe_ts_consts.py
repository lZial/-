"""Подбор констант TimeScaleData."""
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
        r = None
        for x in p.Resources:
            if x.Name == "Бизнес-аналитик":
                r = x
                break
        a = p.ProjectStart
        b = a + datetime.timedelta(days=40)
        for typ in range(0, 16):
            for unit in range(0, 8):
                try:
                    vals = r.TimeScaleData(a, b, typ, unit, 1)
                    n = vals.Count
                    first = vals(1).Value if n else None
                    say("type=%d unit=%d -> ok count=%d first=%r"
                        % (typ, unit, n, first))
                except Exception:
                    pass
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
