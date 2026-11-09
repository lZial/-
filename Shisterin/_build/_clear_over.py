"""Попытка снять Overallocated: запас MaxUnits + пересчёт + UI-действия."""
import os, sys, time
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'.')
import paths
from reshoot_fixed import Shot, say

def fix(fp, bumps, label):
    paths.MPP=fp; s=Shot()
    try:
        p=s.app.ActiveProject
        for r in p.Resources:
            if r.Name in bumps:
                for i in range(1,r.Availabilities.Count+1):
                    r.Availabilities(i).AvailableUnit=bumps[r.Name]*100.0
                r.MaxUnits=bumps[r.Name]
        s.app.CalculateProject()
        # try COM leveling clear variants
        for expr in [
            ('LevelClear', lambda: s.app.LevelClear()),
            ('ClearLeveling()', lambda: s.app.ClearLeveling()),
            ('ResourceLevelingNow', lambda: s.app.ResourceLeveling(True)),
        ]:
            name,fn=expr
            try: fn(); say(name,'ok')
            except Exception as e: say(name,'err',str(e)[:70])
        try: s.app.LevelNow(False)
        except: pass
        s.app.CalculateProject()
        flags=[r.Name for r in p.Resources if r.Type==0 and r.Overallocated]
        tasks=[t.ID for t in p.Tasks if t.Overallocated]
        say(label,'flags',flags,'tasks',tasks)
        s.app.FileSave()
    finally:
        try: s.app.FileQuit()
        except: pass

fix(r'D:\UP_MobileBank\УП_Шистерин.mpp',
    {'Бизнес-аналитик':2.0,'Бэкенд-разработчик':4.0,'DevOps-инженер':2.0,'Тестировщик':5.0}, 'SH')
fix(r'D:\UP_NeuralDefects\УП_Матвих.mpp',
    {'ML-инженер':5.0,'CV-инженер':3.0,'DevOps-инженер':2.0,'Тестировщик':4.0}, 'MA')
