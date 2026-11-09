"""Пересоздание назначений проблемных задач."""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say

SRC = os.path.join(paths.BASE, "УП_Шистерин.mpp")
TEST = os.path.join(paths.BUILD, "test_reassign.mpp")
TASK_IDS = (64, 67, 78)


def main():
    shutil.copy2(SRC, TEST)
    paths.MPP = TEST
    s = Shot()
    try:
        p = s.app.ActiveProject
        say("до:", [r.Name for r in p.Resources if r.Type == 0 and r.Overallocated],
            [t.ID for t in p.Tasks if t.Overallocated])
        for t in p.Tasks:
            if t.ID not in TASK_IDS:
                continue
            saved = []
            for a in t.Assignments:
                saved.append((a.ResourceID, a.ResourceName, a.Units, a.Work))
            say("T%s %s: %d назначений" % (t.ID, t.Name[:40], len(saved)))
            for a in list(t.Assignments):
                a.Delete()
            for rid, rname, units, work in saved:
                a = t.Assignments.Add(t.ID, rid, units)
                if work:
                    a.Work = work
                say("   + %-24s %.0f%% %.1fч" % (rname, units * 100, work / 60.0))
        s.app.CalculateProject()
        say("после:", [r.Name for r in p.Resources if r.Type == 0 and r.Overallocated],
            [t.ID for t in p.Tasks if t.Overallocated])
        say("финиш:", str(p.ProjectFinish)[:10], "бюджет:", p.Cost)
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
