"""Интроспекция объекта Availability в MS Project."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say

TEST = os.path.join(paths.BUILD, "test_fix2.mpp")


def main():
    paths.MPP = TEST
    s = Shot()
    try:
        pr = s.app.ActiveProject
        r = None
        for x in pr.Resources:
            if x.Name == "Мобильный разработчик":
                r = x
                break
        say("resource", r.Name, "MaxUnits", r.MaxUnits,
            "avail count", r.Availabilities.Count)
        a = r.Availabilities(1)
        say("dir avail:", [n for n in dir(a) if not n.startswith("_")])
        for prop in ("AvailableFrom", "AvailableTo", "AvailableUnits",
                     "Units", "Start", "Finish"):
            try:
                say("  get %s = %r" % (prop, getattr(a, prop)))
            except Exception as e:
                say("  get %s ERR %s" % (prop, str(e)[:80]))
        # пробуем записать
        import datetime
        for prop, val in (("AvailableUnits", 4.0),
                          ("AvailableFrom", datetime.datetime(2026, 2, 2)),
                          ("AvailableTo", datetime.datetime(2026, 8, 17))):
            try:
                setattr(a, prop, val)
                say("  set %s = %r -> OK" % (prop, val))
            except Exception as e:
                say("  set %s ERR %s" % (prop, str(e)[:100]))
        say("after: MaxUnits", r.MaxUnits, "Overallocated", r.Overallocated)
        say("tasks overallocated:", sum(1 for t in pr.Tasks if t.Overallocated))
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
