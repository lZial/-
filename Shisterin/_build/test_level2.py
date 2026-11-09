"""Проверка гипотезы о дробном пике: небольшой запас лимита."""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say

SRC = os.path.join(paths.BASE, "УП_Шистерин.mpp")
TEST = os.path.join(paths.BUILD, "test_level2.mpp")

BUMP = {
    "Бизнес-аналитик": 1.01,
    "Бэкенд-разработчик": 3.51,
    "DevOps-инженер": 1.01,
    "Тестировщик": 4.01,
    "Мобильный разработчик": 4.01,
}


def main():
    shutil.copy2(SRC, TEST)
    paths.MPP = TEST
    s = Shot()
    try:
        p = s.app.ActiveProject
        for r in p.Resources:
            if r.Name in BUMP:
                say("до %-26s Max=%.4f Peak=%.4f Over=%s"
                    % (r.Name, r.MaxUnits, r.PeakUnits, r.Overallocated))
                for i in range(1, r.Availabilities.Count + 1):
                    r.Availabilities(i).AvailableUnit = BUMP[r.Name] * 100.0
                r.MaxUnits = BUMP[r.Name]
                say("после %-24s Max=%.4f Over=%s"
                    % (r.Name, r.MaxUnits, r.Overallocated))
        s.app.CalculateProject()
        over_r = [r.Name for r in p.Resources if r.Type == 0 and r.Overallocated]
        over_t = [t.ID for t in p.Tasks if t.Overallocated]
        say("итог: ресурсов", len(over_r), over_r, "задач", len(over_t), over_t)
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
