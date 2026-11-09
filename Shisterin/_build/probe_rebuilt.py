"""Сводная проверка пересобранного проекта."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say


def main():
    s = Shot()
    try:
        pr = s.app.ActiveProject
        say("файл:", pr.Name)
        say("задач:", pr.Tasks.Count)
        say("начало:", pr.ProjectStart)
        say("окончание:", pr.ProjectFinish)
        say("дата отчётности:", pr.StatusDate)
        say("бюджет:", pr.Cost)
        say("БСЗР/БСВР/ФСВР:", pr.BCWS, pr.BCWP, pr.ActualCost)
        over_r = [r.Name for r in pr.Resources if r.Type == 0 and r.Overallocated]
        over_t = [t.ID for t in pr.Tasks if t.Overallocated]
        say("перегружено ресурсов:", len(over_r), over_r)
        say("перегружено задач:", len(over_t))
        mt = [t for t in pr.Tasks if "Совещание" in str(t.Name)]
        say("совещаний:", len(mt),
            "| первое:", str(mt[1].Start)[:10] if len(mt) > 1 else "-",
            "| последнее:", str(mt[-1].Start)[:10] if len(mt) > 1 else "-")
    finally:
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
