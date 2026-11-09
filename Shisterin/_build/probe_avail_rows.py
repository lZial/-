"""Просмотр строк доступности ресурсов (AvailableUnit)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say

TEST = os.path.join(paths.BUILD, "test_fix2.mpp")


def fmt(d):
    try:
        return str(d)[:16]
    except Exception:
        return str(d)


def main():
    paths.MPP = TEST
    s = Shot()
    try:
        pr = s.app.ActiveProject
        for r in pr.Resources:
            if r.Type != 0:
                continue
            say("%-28s Max=%r Over=%s rows=%d"
                % (r.Name, r.MaxUnits, r.Overallocated, r.Availabilities.Count))
            for i in range(1, r.Availabilities.Count + 1):
                a = r.Availabilities(i)
                try:
                    u = a.AvailableUnit
                except Exception as e:
                    u = "ERR " + str(e)[:40]
                say("    %d) %s .. %s  unit=%r"
                    % (i, fmt(a.AvailableFrom), fmt(a.AvailableTo), u))
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
