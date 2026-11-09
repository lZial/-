"""Тест: установка MaxUnits без удаления окон доступности."""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say

SRC = os.path.join(paths.BASE, "УП_Шистерин.mpp")
TEST = os.path.join(paths.BUILD, "test_fix2.mpp")

TARGET = {
    "Руководитель проекта": 0.5,
    "Бизнес-аналитик": 1.0,
    "Аналитик требований": 1.0,
    "Архитектор": 1.0,
    "UX/UI-дизайнер": 1.0,
    "Мобильный разработчик": 4.0,
    "Бэкенд-разработчик": 3.5,
    "DevOps-инженер": 1.0,
    "Тестировщик": 4.0,
    "Специалист по ИБ": 1.0,
    "Аналитик данных": 1.0,
    "Технический директор": 0.3,
    "Технический писатель": 0.5,
    "Маркетолог": 1.0,
}


def main():
    shutil.copy2(SRC, TEST)
    paths.MPP = TEST
    s = Shot()
    try:
        pr = s.app.ActiveProject
        for r in pr.Resources:
            if r.Type != 0 or r.Name not in TARGET:
                continue
            say("%-28s было MaxUnits=%r avail=%d"
                % (r.Name, r.MaxUnits, r.Availabilities.Count))
            r.MaxUnits = TARGET[r.Name]
            say("     стало MaxUnits=%r" % (r.MaxUnits,))
        over_r = [r.Name for r in pr.Resources
                  if r.Type == 0 and r.Overallocated]
        over_t = sum(1 for t in pr.Tasks if t.Overallocated)
        say("перегружено ресурсов:", len(over_r), over_r)
        say("перегружено задач:", over_t)
        pr.Save()
        say("сохранено:", TEST)
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
