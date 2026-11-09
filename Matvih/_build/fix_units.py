"""Исправляет максимальные единицы и окна доступности ресурсов.

В MS Project свойство MaxUnits задаётся долей (2.0 = 200 %), а
Availability.AvailableUnit — целым числом процентов (200 = 200 %).
При сборке проекта в окна доступности были записаны доли, поэтому
в листе ресурсов отображалось 0 %. Скрипт пересоздаёт окна доступности
в процентах и выставляет MaxUnits.
"""
import datetime
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
import win32com.client as w

# имя: (доля MaxUnits, начало окна, конец окна, процент доступности)
UNITS = {
    "Руководитель проекта": (0.5, None, None, None),
    "Бизнес-аналитик": (1.0, None, None, None),
    "Аналитик требований": (1.0, None, None, None),
    "Архитектор": (1.0, datetime.date(2026, 2, 2), datetime.date(2026, 6, 30), 100),
    "Дизайнер интерфейсов": (1.0, None, None, None),
    "ML-инженер": (2.0, datetime.date(2026, 2, 2), datetime.date(2026, 6, 30), 200),
    "CV-инженер": (1.5, datetime.date(2026, 2, 16), datetime.date(2026, 6, 30), 150),
    "DevOps-инженер": (1.0, None, None, None),
    "Тестировщик": (1.5, datetime.date(2026, 3, 2), datetime.date(2026, 6, 30), 150),
    "Специалист по ИБ": (1.0, datetime.date(2026, 2, 16), datetime.date(2026, 5, 29), 100),
    "Аналитик данных": (1.0, None, None, None),
    "Технический директор": (0.3, None, None, None),
    "Технический писатель": (0.5, datetime.date(2026, 5, 18), datetime.date(2026, 6, 30), 50),
    "Инженер по внедрению": (1.0, datetime.date(2026, 5, 4), datetime.date(2026, 7, 31), 100),
}


def fix(path):
    app = w.Dispatch("MSProject.Application")
    app.Visible = False
    app.DisplayAlerts = 0
    app.FileOpen(path)
    p = app.ActiveProject
    print("файл:", p.Name, flush=True)
    for r in p.Resources:
        name = (r.Name or "").strip()
        if name not in UNITS:
            continue
        units, d1, d2, pct = UNITS[name]
        # удаляем прежние окна доступности (с конца)
        try:
            for j in range(r.Availabilities.Count, 0, -1):
                r.Availabilities.Item(j).Delete()
        except Exception as e:
            print("  ! удалить окна %s: %s" % (name, str(e)[:70]))
        if d1 is not None:
            a = r.Availabilities.Add(datetime.datetime(d1.year, d1.month, d1.day),
                                     datetime.datetime(d2.year, d2.month, d2.day),
                                     pct)
            print("  %-24s окно %s..%s = %d %%" % (
                name, d1.strftime("%d.%m.%Y"), d2.strftime("%d.%m.%Y"),
                a.AvailableUnit), flush=True)
        r.MaxUnits = units
        print("  %-24s MaxUnits=%.2f" % (name, r.MaxUnits), flush=True)
    p.SaveAs(path)
    time.sleep(2)
    app.FileClose(0)
    app.FileQuit()
    time.sleep(2)


def main():
    for path in (paths.MPP, paths.EXP_MPP):
        if os.path.exists(path):
            fix(path)
    # контроль
    app = w.Dispatch("MSProject.Application")
    app.Visible = False
    app.DisplayAlerts = 0
    app.FileOpen(paths.MPP)
    p = app.ActiveProject
    for i in (6, 7, 9, 1):
        r = p.Resources.Item(i)
        print("контроль:", r.Name, "MaxUnits=", r.MaxUnits,
              "окон:", r.Availabilities.Count)
    app.FileClose(0)
    app.FileQuit()


if __name__ == "__main__":
    main()
