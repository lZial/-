"""Дамп задач и ресурсов текущего плана в tasks.tsv / resources.tsv.

Только чтение свойств (никаких диалоговых методов), затем закрытие файла
и FileQuit.
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
import win32com.client as w

app = w.Dispatch("MSProject.Application")
app.Visible = False
app.DisplayAlerts = 0
app.FileOpen(paths.MPP)
time.sleep(2)
p = app.ActiveProject
print("проект:", p.Name)

task_header = ["ID", "Уровень", "Наименование", "Длительность", "Начало", "Окончание",
               "Предшественники", "Ресурсы", "Трудозатраты", "Затраты", "Тип",
               "Ограничение", "Веха", "%Выполнения", "Число1", "Число2", "Длительность1"]
with open(os.path.join(paths.BUILD, "tasks.tsv"), "w", encoding="utf-8") as f:
    f.write("\t".join(task_header) + "\n")
    for i in range(1, p.Tasks.Count + 1):
        t = p.Tasks.Item(i)
        f.write("\t".join([
            str(t.ID), str(t.OutlineLevel), t.Name, str(t.Duration),
            str(t.Start), str(t.Finish), str(t.Predecessors), str(t.ResourceNames),
            str(t.Work), str(t.Cost), str(t.Type), str(t.ConstraintType),
            str(t.Milestone), str(t.PercentComplete),
            str(t.Number1), str(t.Number2), str(t.Duration1)]) + "\n")

res_header = ["ID", "Имя", "Инициалы", "Группа", "Тип", "Макс. единиц",
              "Стандартная ставка", "Ставка сверхурочных", "Начало доступности",
              "Конец доступности", "Трудозатраты", "Затраты", "%Выполнения"]
with open(os.path.join(paths.BUILD, "resources.tsv"), "w", encoding="utf-8") as f:
    f.write("\t".join(res_header) + "\n")
    for i in range(1, p.Resources.Count + 1):
        r = p.Resources.Item(i)
        f.write("\t".join([
            str(r.ID), r.Name, str(r.Initials), str(r.Group), str(r.Type),
            str(r.MaxUnits), str(r.StandardRate), str(r.OvertimeRate),
            str(r.AvailableFrom), str(r.AvailableTo), str(r.Work), str(r.Cost),
            str(r.PercentWorkComplete)]) + "\n")

summ = sum(1 for i in range(1, p.Tasks.Count + 1) if p.Tasks.Item(i).Summary)
work = p.Tasks.Count - summ
meet = [p.Tasks.Item(i).Name for i in range(1, p.Tasks.Count + 1)
        if "Совещание" in p.Tasks.Item(i).Name]
print("задач: %d (сводных %d, рабочих %d)" % (p.Tasks.Count, summ, work))
print("совещаний:", len(meet))
print("ресурсов:", p.Resources.Count)
print("начало:", p.ProjectStart, "окончание:", p.ProjectFinish)
print("бюджет:", p.Cost)
app.FileClose(0)
time.sleep(1)
app.FileQuit()
print("готово")
