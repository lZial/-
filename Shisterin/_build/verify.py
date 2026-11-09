"""Итоговая проверка всех материалов."""
import os
import sys
import time

import win32com.client as w

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths

BASE = paths.BASE
MPP = paths.MPP
EXP = paths.EXP_MPP
DOC = paths.DOC
SHOTS = paths.SHOTS

print("=" * 70)
print("1. ФАЙЛ ПРОЕКТА MS PROJECT")
app = w.Dispatch("MSProject.Application")
app.Visible = False
app.DisplayAlerts = 0
app.FileOpen(MPP)
p = app.ActiveProject
tasks = p.Tasks.Count
res = p.Resources.Count
levels = {}
types = {}
cons = {}
mil = 0
for i in range(1, tasks + 1):
    t = p.Tasks.Item(i)
    levels[t.OutlineLevel] = levels.get(t.OutlineLevel, 0) + 1
    types[t.Type] = types.get(t.Type, 0) + 1
    cons[t.ConstraintType] = cons.get(t.ConstraintType, 0) + 1
    if t.Milestone:
        mil += 1
print("   файл           :", os.path.basename(MPP), "(%d КБ)" % (os.path.getsize(MPP) // 1024))
print("   задач          :", tasks, "| сводных(ур.1):", levels.get(1, 0),
      "| рабочих(ур.2):", levels.get(2, 0))
print("   вех            :", mil)
print("   ресурсов       :", res)
print("   начало/оконч.  :", str(p.ProjectStart)[:10], "/", str(p.ProjectFinish)[:10])
print("   бюджет         :", p.Cost, "руб.")
print("   типы задач     :", types, "(1 = фиксированная длительность)")
print("   ограничения    :", {k: v for k, v in cons.items() if k != 0}, "(0 = по умолчанию)")
print("   базовый план   :", str(p.BaselineSavedDate(0))[:10])
print("   дата отчётности:", str(p.StatusDate)[:10])
print("   БСЗР/БСВР/ФСВР :", p.BCWS, "/", p.BCWP, "/", p.ActualCost)
print("   ОКП/ОПС        :", p.SV, "/", p.CostVariance)
app.FileOpen(EXP)
e = app.ActiveProject
print("   эксперимент    : бюджет %s руб. (базовый %s)" % (e.Cost, p.Cost))
app.FileQuit()

print()
print("2. ОТЧЁТ WORD")
app2 = w.Dispatch("Word.Application")
app2.Visible = False
app2.DisplayAlerts = 0
d = app2.Documents.Open(DOC)
print("   файл           :", os.path.basename(DOC), "(%d КБ)" % (os.path.getsize(DOC) // 1024))
print("   формат         :", "Word 97-2003 (.doc)" if d.SaveFormat == 0 else d.SaveFormat)
print("   страниц        :", d.ComputeStatistics(2))
print("   слов           :", d.ComputeStatistics(0))
print("   рисунков       :", d.InlineShapes.Count)
print("   таблиц         :", d.Tables.Count)
print("   оглавление     :", d.TablesOfContents.Count, "раздел(а)")
try:
    ps = d.PageSetup
    print("   поля (см)      : left %.2f right %.2f top %.2f bottom %.2f" % (
        ps.LeftMargin / 28.3465, ps.RightMargin / 28.3465,
        ps.TopMargin / 28.3465, ps.BottomMargin / 28.3465))
    print("   колонтитулы    : header %.2f см, footer %.2f см, без колонтитулов на 1-й стр.: %s" % (
        ps.HeaderDistance / 28.3465, ps.FooterDistance / 28.3465,
        bool(ps.DifferentFirstPageHeaderFooter)))
except Exception as e:
    print("   параметры страницы: err", e)
d.Close(SaveChanges=0)
app2.Quit()

print()
print("3. СКРИНШОТЫ")
files = sorted(os.listdir(SHOTS))
print("   количество      :", len(files))
print("   общий объём     : %.1f МБ" % (sum(os.path.getsize(os.path.join(SHOTS, f))
                                        for f in files) / 1048576.0))
print("=" * 70)
