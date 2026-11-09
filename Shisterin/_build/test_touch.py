"""Способы сбросить устаревший флаг Overallocated."""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say

SRC = os.path.join(paths.BASE, "УП_Шистерин.mpp")
TEST = os.path.join(paths.BUILD, "test_touch.mpp")


def flags(p):
    return ([r.Name for r in p.Resources if r.Type == 0 and r.Overallocated],
            [t.ID for t in p.Tasks if t.Overallocated])


def main():
    shutil.copy2(SRC, TEST)
    paths.MPP = TEST
    s = Shot()
    try:
        p = s.app.ActiveProject
        say("старт:", flags(p))
        for r in p.Resources:
            if r.Type == 0 and r.Overallocated:
                say("  %-24s AvailFrom=%s AvailTo=%s"
                    % (r.Name, str(getattr(r, "AvailableFrom", "?"))[:10],
                       str(getattr(r, "AvailableTo", "?"))[:10]))
        # 1. коснуться назначений
        for r in p.Resources:
            if r.Type != 0 or not r.Overallocated:
                continue
            for a in r.Assignments:
                a.Units = a.Units
        s.app.CalculateProject()
        say("после касания назначений:", flags(p))
        # 2. покачать MaxUnits
        for r in p.Resources:
            if r.Type != 0 or not r.Overallocated:
                continue
            m = r.MaxUnits
            r.MaxUnits = m * 0.99
            r.MaxUnits = m
        s.app.CalculateProject()
        say("после покачки MaxUnits:", flags(p))
        # 3. снять выравнивание и выровнять заново
        try:
            s.app.LevelClear()
            say("LevelClear ok")
        except Exception as e:
            say("LevelClear ERR", str(e)[:80])
        s.app.LevelingOptions(False, True, True, 1, True,
                              p.ProjectStart, p.ProjectFinish,
                              0, True, True, False)
        s.app.LevelNow(True)
        say("после LevelClear+LevelNow:", flags(p))
        # 4. сохранить и перечитать
        s.app.FileSave()
        say("сохранено")
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
