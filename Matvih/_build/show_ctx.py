import sys

sys.stdout.reconfigure(encoding="utf-8")
s = open("works.py", encoding="utf-8").read()
for n in sys.argv[1:] or ("11_",):
    i = s.find(n)
    if i < 0:
        print(n, "NOT FOUND")
        continue
    start = max(0, i - 900)
    print("=" * 70)
    print(s[start:i + 140].replace("\n", " | "))
