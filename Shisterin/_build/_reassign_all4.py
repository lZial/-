"""Пересоздать все назначения проблемных ресурсов (копия)."""
import os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
import paths
from reshoot_fixed import Shot, say

NAMES = {"Бизнес-аналитик", "Бэкенд-разработчик", "DevOps-инженер", "Тестировщик"}
SRC = os.path.join(paths.BASE, "УП_Шистерин.mpp")
TEST = os.path.join(paths.BUILD, "test_reassign4.mpp")
shutil.copy2(SRC, TEST)
paths.MPP = TEST
s = Shot()
try:
    p = s.app.ActiveProject
    say("before", [r.Name for r in p.Resources if r.Type == 0 and r.Overallocated], [t.ID for t in p.Tasks if t.Overallocated])
    for r in p.Resources:
        if r.Name not in NAMES:
            continue
        saved = [(a.TaskID, a.Units, a.Work) for a in r.Assignments]
        say(r.Name, "assignments:", len(saved))
        for a in list(r.Assignments):
            a.Delete()
        for tid, units, work in saved:
            a = p.Tasks.UniqueID  # dummy
            na = p.Tasks.Item(tid).Assignments.Add(tid, r.ID, units)
            if work:
                na.Work = work
    s.app.CalculateProject()
    say("after calc", [r.Name for r in p.Resources if r.Type == 0 and r.Overallocated], [t.ID for t in p.Tasks if t.Overallocated])
    s.app.FileSave()
    say("finish/cost:", str(p.ProjectFinish)[:10], p.Cost)
finally:
    try: s.app.FileQuit()
    except Exception: pass
