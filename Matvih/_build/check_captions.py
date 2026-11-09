"""Проверка PDF: подписи «Рисунок», не имеющие изображения выше на той же странице."""
import re
import sys

import pymupdf

sys.stdout.reconfigure(encoding="utf-8")
doc = pymupdf.open(r"D:\UP_NeuralDefects\УП_Матвих.pdf")
pat = re.compile(r"Рисунок\s+[\d\.А-Я]+")
for i, page in enumerate(doc, 1):
    info = page.get_text("dict")
    images = []
    caps = []
    for b in info["blocks"]:
        if b["type"] == 1:
            images.append(b["bbox"][1])
        else:
            txt = " ".join(s["text"] for l in b["lines"] for s in l["spans"])
            if pat.search(txt) and "Рисунок" in txt:
                caps.append((b["bbox"][1], txt.strip()))
    for y, t in caps:
        above = [iy for iy in images if iy < y]
        if not above:
            print("стр. %2d y=%4.0f %s" % (i, y, t.replace("\n", " ")[:80]))
print("готово, страниц:", doc.page_count)
