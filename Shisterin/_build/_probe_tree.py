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
    from collections import Counter
    cnt = Counter()
    n = 0
    for d in s.mp.descendants():
        n += 1
        try:
            ct = getattr(d.element_info, "control_type", "?")
            cnt[ct] += 1
            if n <= 120:
                t = d.window_text()
                if t.strip():
                    say(" ", ct, repr(t.strip()[:60]))
        except Exception:
            pass
    say("total elements:", n)
    for k, v in cnt.most_common():
        say("  type", k, v)
    capture(s.hwnd, os.path.join(paths.BUILD, "_tree.png"))
finally:
    try:
        s.app.FileQuit()
    except Exception:
        pass
say("done")
