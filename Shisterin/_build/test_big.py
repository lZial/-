"""Тест завышенных лимитов + сохранение/переоткрытие."""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say

SRC = os.path.join(paths.BASE, "УП_Шистерин.mpp")
TEST = os.path.join(paths.BUILD, "test_big.mpp")

BIG = {
    "Бизнес-аналитик": 2.0,
    "Бэкенд-разработчик": 5.0,
    "DevOps-инженер": 2.0,
    "Тестировщик": 6.0,
    "Мобильный разработчик": 5.0,
}


def main():
    shutil.copy2(SRC, TEST)
    paths.MPP = TEST
    s = Shot()
    try:
        p = s.app.ActiveProject
        for r in p.Resources:
            if r.Name in BIG:
                for i in range(1, r.Availabilities.Count + 1):
                    r.Availabilities(i).AvailableUnit = BIG[r.Name] * 100.0
                r.MaxUnits = BIG[r.Name]
        say("после установки:",
            [r.Name for r in p.Resources if r.Type == 0 and r.Overallocated])
        s.app.FileSave()
        say("сохранено")
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
