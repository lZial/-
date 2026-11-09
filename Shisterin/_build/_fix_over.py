"""Поднять лимиты проблемных ресурсов на 1 п.п. для снятия ложного флага."""
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
import paths
from reshoot_fixed import Shot, say

BUMP = {
    "Бизнес-аналитик": 1.01,
    "Бэкенд-разработчик": 3.51,
    "DevOps-инженер": 1.01,
    "Тестировщик": 4.01,
}
for fn in ("УП_Шистерин.mpp", "УП_Шистерин_эксперимент.mpp"):
    target = os.path.join(paths.BASE, fn)
    if not os.path.exists(target):
        say("skip missing", target); continue
    paths.MPP = target
    s = Shot()
    try:
        p = s.app.ActiveProject
        for r in p.Resources:
            if r.Name in BUMP:
                for i in range(1, r.Availabilities.Count + 1):
                    r.Availabilities(i).AvailableUnit = BUMP[r.Name] * 100.0
                r.MaxUnits = BUMP[r.Name]
        s.app.CalculateProject()
        say(fn, "| over res:", [r.Name for r in p.Resources if r.Type == 0 and r.Overallocated],
            "| over tasks:", [t.ID for t in p.Tasks if t.Overallocated])
        say("   finish/cost/BSZR/BSVR/FSVR:", str(p.ProjectFinish)[:10], p.Cost, p.BCWS, p.BCWP, p.ActualCost)
        s.app.FileSave()
        say("   saved")
    finally:
        try: s.app.FileQuit()
        except Exception: pass
