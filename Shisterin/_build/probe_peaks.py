"""Пики загрузки ресурсов в test_fix4.mpp и детали перегруженной задачи."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say

TEST = os.path.join(paths.BUILD, "test_fix4.mpp")


def main():
    paths.MPP = TEST
    s = Shot()
    try:
        pr = s.app.ActiveProject
        say("=== ПИКИ РЕСУРСОВ ===")
        for r in pr.Resources:
            if r.Type != 0:
                continue
            if r.PeakUnits > r.MaxUnits + 0.001 or r.Overallocated:
                say("%-28s Max=%.0f%% Peak=%.0f%% Over=%s"
                    % (r.Name, r.MaxUnits * 100, r.PeakUnits * 100,
                       r.Overallocated))
        say()
        say("=== ПЕРЕГРУЖЕННЫЕ ЗАДАЧИ ===")
        for t in pr.Tasks:
            if not t.Overallocated:
                continue
            say("ID %s %s %s..%s"
                % (t.ID, t.Name, str(t.Start)[:10], str(t.Finish)[:10]))
            for a in t.Assignments:
                say("    %-28s %.0f%% work=%.1fч"
                    % (a.ResourceName, a.Units * 100, a.Work / 60.0))
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
