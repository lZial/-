# -*- coding: utf-8 -*-
"""Готовит копии планов с праздниками 2027 для съёмки календарей.

Оригинальные файлы не меняются: съёмка идёт с копий _cal_shot*.mpp.
"""
import datetime as dt
import shutil
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
import win32com.client

JOBS = [
    r"D:\UP_MobileBank\УП_Шистерин.mpp",
    r"D:\UP_MobileBank\УП_Шистерин_эксперимент.mpp",
]

HOL = [
    (dt.datetime(2027, 1, 1), dt.datetime(2027, 1, 1)),
    (dt.datetime(2027, 1, 2), dt.datetime(2027, 1, 2)),
    (dt.datetime(2027, 1, 5), dt.datetime(2027, 1, 8)),
    (dt.datetime(2027, 2, 23), dt.datetime(2027, 2, 23)),
    (dt.datetime(2027, 3, 8), dt.datetime(2027, 3, 8)),
    (dt.datetime(2027, 5, 1), dt.datetime(2027, 5, 1)),
    (dt.datetime(2027, 5, 9), dt.datetime(2027, 5, 9)),
    (dt.datetime(2027, 6, 12), dt.datetime(2027, 6, 12)),
    (dt.datetime(2027, 11, 4), dt.datetime(2027, 11, 4)),
]
# Project хранит даты исключений в UTC: при передаче локальной даты
# в списке отображается предыдущий день, поэтому сдвигаем на +1.
SHIFT = dt.timedelta(days=1)


def log(*a):
    print(*a, flush=True)


for src in JOBS:
    dst = src.replace(".mpp", ".mpp").replace(
        "УП_Шистерин.mpp", "_cal_shot.mpp").replace(
        "УП_Шистерин_эксперимент.mpp", "_cal_shot_exp.mpp")
    dst = r"D:\UP_MobileBank\_build" + "\\" + dst.split("\\")[-1]
    shutil.copy2(src, dst)
    app = win32com.client.DispatchEx("MSProject.Application")
    app.Visible = False
    app.DisplayAlerts = False
    try:
        app.FileOpen(dst)
        pr = app.ActiveProject
        cal = pr.BaseCalendars("Стандартный")
        while cal.Exceptions.Count:
            cal.Exceptions(1).Delete()
        for a, b in HOL:
            cal.Exceptions.Add(1, a + SHIFT, b + SHIFT)
        app.FileSave()
        log(dst, "исключений:", cal.Exceptions.Count,
            "финиш:", pr.ProjectFinish,
            "стоимость:", pr.ProjectSummaryTask.Cost)
        app.FileClose(False)
    finally:
        try:
            app.Quit()
        except Exception:
            pass
    time.sleep(3)
log("done")
