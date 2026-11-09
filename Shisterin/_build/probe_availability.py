"""Сырые значения доступности ресурсов проекта Шистерина."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reshoot_fixed import Shot, say


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
            if r.Type != 0:          # только трудовые
                continue
            say("ID %-2s %-30s MaxUnits=%r Peak=%r Over=%s"
                % (r.ID, r.Name, r.MaxUnits, r.PeakUnits, r.Overallocated))
            try:
                for i in range(1, r.Availabilities.Count + 1):
                    a = r.Availabilities(i)
                    say("     avail %d: %s .. %s units=%r"
                        % (i, fmt(a.AvailableFrom), fmt(a.AvailableTo),
                           a.AvailableUnits))
            except Exception as e:
                say("     avail err:", str(e)[:90])
    finally:
        try:
            s.app.ActiveProject.Saved = True
        except Exception:
            pass
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
