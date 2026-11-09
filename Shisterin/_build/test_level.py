"""Тест выравнивания на копии пересобранного проекта."""
import datetime
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say

SRC = os.path.join(paths.BASE, "УП_Шистерин.mpp")
TEST = os.path.join(paths.BUILD, "test_level.mpp")


def main():
    shutil.copy2(SRC, TEST)
    paths.MPP = TEST
    s = Shot()
    try:
        p = s.app.ActiveProject
        say("до: окончание %s бюджет %s" % (str(p.ProjectFinish)[:10], p.Cost))
        s.app.LevelingOptions(False, True, True, 1, True,
                              datetime.datetime(2025, 1, 1),
                              datetime.datetime(2025, 12, 31),
                              0, True, True, False)
        s.app.LevelNow(True)
        say("после: окончание %s бюджет %s"
            % (str(p.ProjectFinish)[:10], p.Cost))
        over_r = [r.Name for r in p.Resources if r.Type == 0 and r.Overallocated]
        over_t = [t.ID for t in p.Tasks if t.Overallocated]
        say("перегружено ресурсов:", len(over_r), over_r)
        say("перегружено задач:", len(over_t), over_t)
        s.app.CalculateProject()
        over_r = [r.Name for r in p.Resources if r.Type == 0 and r.Overallocated]
        over_t = [t.ID for t in p.Tasks if t.Overallocated]
        say("после пересчёта:", len(over_r), over_r, len(over_t), over_t)
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
