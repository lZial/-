"""Разведка COM-коллекции отчетов MS Project."""
import os
import sys
import time

import win32com.client as w

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths


def say(*a):
    print(*a, flush=True)


def main():
    app = w.Dispatch("MSProject.Application")
    app.Visible = False
    app.DisplayAlerts = 0
    app.FileOpen(paths.MPP)
    time.sleep(3)
    for expr in ("app.Reports()", "app.ActiveProject.Reports()"):
        try:
            r = eval(expr)
            say(expr, "->", r, "count", r.Count)
            for i in range(1, r.Count + 1):
                rep = r.Item(i)
                fields = []
                for f in ("Name", "Title", "Type", "Index"):
                    try:
                        fields.append("%s=%r" % (f, getattr(rep, f)))
                    except Exception:
                        pass
                say("   ", i, "; ".join(fields))
        except Exception as e:
            say(expr, "ERR", str(e)[:180])
    try:
        say("ReportPrint args?", app.ReportPrint.__doc__)
    except Exception as e:
        say("doc err", str(e)[:100])
    try:
        app.FileQuit()
    except Exception:
        pass


if __name__ == "__main__":
    main()
