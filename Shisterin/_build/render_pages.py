"""Рендер страниц PDF в PNG для просмотра вёрстки."""
import os
import sys

import pymupdf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths

out = os.path.join(paths.BUILD, "_pages")
os.makedirs(out, exist_ok=True)
doc = pymupdf.open(paths.PDF)
print("страниц:", doc.page_count)
for i, page in enumerate(doc, 1):
    pix = page.get_pixmap(dpi=110)
    pix.save(os.path.join(out, "p%02d.png" % i))
print("готово:", out)
