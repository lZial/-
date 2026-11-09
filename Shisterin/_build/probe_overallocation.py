"""Диагностика превышения доступности ресурсов в проекте Шистерина."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reshoot_fixed import Shot, say


def main():
    s = Shot()
    try:
        pr = s.app.ActiveProject
        say("проект:", pr.Name)
        say("дата отчётности:", pr.StatusDate)
        say()
        say("=== РЕСУРСЫ С ПЕРЕГРУЗКОЙ ===")
        for r in pr.Resources:
            try:
                if not r.Overallocated:
                    continue
                say("ID %-3s %-32s max=%.0f%% peak=%.0f%% type=%s"
                    % (r.ID, r.Name, r.MaxUnits * 100, r.PeakUnits * 100,
                       r.Type))
                for a in r.Assignments:
                    say("     задача %-4s %-55s units=%.0f%% work=%.1fч"
                        % (a.TaskID, a.TaskName[:55], a.Units * 100,
                           a.Work / 60.0))
            except Exception as e:
                say("  res err", getattr(r, "ID", "?"), str(e)[:80])
        say()
        say("=== ЗАДАЧИ С ПЕРЕГРУЗКОЙ ===")
        for t in pr.Tasks:
            try:
                if not t.Overallocated:
                    continue
                say("ID %-3s %-60s %s..%s"
                    % (t.ID, t.Name[:60],
                       str(t.Start)[:10], str(t.Finish)[:10]))
                for a in t.Assignments:
                    say("     %-28s units=%.0f%% work=%.1fч"
                        % (a.ResourceName[:28], a.Units * 100,
                           a.Work / 60.0))
            except Exception as e:
                say("  task err", getattr(t, "ID", "?"), str(e)[:80])
    finally:
        try:
            s.app.ActiveProject.Saved = True
        except Exception:
            pass
        try:
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
