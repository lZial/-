import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
for f in ("works.py", "make_report2.py", "make_report2_part2.py", "make_report.py"):
    s = open(f, encoding="utf-8").read()
    names = re.findall(r"\d\d_[\wА-Яа-я0-9_]+\.png", s)
    uniq = []
    for n in names:
        if n not in uniq:
            uniq.append(n)
    print(f, len(uniq))
    print("  " + ", ".join(uniq))
