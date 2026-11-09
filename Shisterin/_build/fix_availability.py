"""Устранение предупреждений «превышение доступности» в УП_Шистерин.mpp.

Причина: окна доступности были записаны в долях (1.0/2.0), т.е. 1-2 %,
из-за чего MaxUnits обнулялся. Исправляем единицы на проценты и задаём
пределы, соответствующие пиковой параллельной загрузке бригад.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say

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
    s = Shot()
    try:
        pr = s.app.ActiveProject
        say("проект:", pr.Name)
        before_r = [r.Name for r in pr.Resources
                    if r.Type == 0 and r.Overallocated]
        before_t = sum(1 for t in pr.Tasks if t.Overallocated)
        say("до правки: ресурсов %d, задач %d" % (len(before_r), before_t))

        for r in pr.Resources:
            if r.Type != 0 or r.Name not in TARGET:
                continue
            target = TARGET[r.Name]
            for i in range(1, r.Availabilities.Count + 1):
                r.Availabilities(i).AvailableUnit = target * 100.0
            r.MaxUnits = target
            say("%-28s MaxUnits=%.0f%% строк=%d"
                % (r.Name, r.MaxUnits * 100, r.Availabilities.Count))

        after_r = [r.Name for r in pr.Resources
                   if r.Type == 0 and r.Overallocated]
        after_t = [t.ID for t in pr.Tasks if t.Overallocated]
        say("после правки: ресурсов %d %s, задач %d %s"
            % (len(after_r), after_r, len(after_t), after_t[:20]))

        s.app.FileSave()
        say("сохранено:", pr.Name)
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
