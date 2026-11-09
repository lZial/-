# -*- coding: utf-8 -*-
import os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, say, capture

s = Shot()
try:
    s.app.ViewApply("Диаграмма Ганта")
    time.sleep(2.0)
    s.show()
    time.sleep(1.0)
    for d in s.mp.descendants(control_type="DataItem"):
        try:
            say(" ", repr(d.window_text().strip()[:80]))
        except Exception as e:
            say("  err", str(e)[:40])
finally:
    try:
        s.app.FileQuit()
    except Exception:
        pass
say("done")
