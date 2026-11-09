"""Извлечение исходных PNG из готового отчёта .docx в папку «Скриншоты»."""
import os
import re
import shutil
import sys
import zipfile

from docx import Document
from docx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths

BASE = paths.BASE
BUILD = paths.BUILD
SHOTS = paths.SHOTS
DOCX = paths.DOCX

doc = Document(DOCX)
part = doc.part

# карта relId -> имя файла в word/media
rel_map = {}
for rid, rel in part.rels.items():
    if "image" in rel.reltype:
        rel_map[rid] = os.path.basename(rel.target_ref)

body = doc.element.body
items = []
for p in body.iter(qn("w:p")):
    blips = p.findall(".//" + qn("a:blip"))
    if blips:
        for b in blips:
            rid = b.get(qn("r:embed"))
            fn = rel_map.get(rid)
            if fn:
                items.append(("IMG", fn))
    else:
        txt = "".join(t.text or "" for t in p.findall(".//" + qn("w:t")))
        if txt.strip():
            items.append(("TXT", txt.strip()))

# сопоставляем изображение с подписью (следующий абзац «Рисунок N – ...»)
result = []
for i, (kind, val) in enumerate(items):
    if kind != "IMG":
        continue
    cap = ""
    for j in range(i + 1, min(i + 4, len(items))):
        if items[j][0] == "TXT" and items[j][1].startswith("Рисунок"):
            cap = items[j][1]
            break
    result.append((val, cap))

# имя файла = часть после «Рисунок N – » -> нам нужно исходное имя;
# сопоставляем по порядковому номеру с файлами из папки скриншотов (если есть)
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_report import WORKS

ordered = []
for w in WORKS:
    for img, cap in w["images"]:
        ordered.append((img, cap))
print("ожидается изображений:", len(ordered), " найдено в документе:", len(result))

os.makedirs(SHOTS, exist_ok=True)
with zipfile.ZipFile(DOCX) as z:
    for idx, ((name, cap), (media, dcap)) in enumerate(zip(ordered, result)):
        with z.open("word/media/" + media) as src, \
                open(os.path.join(SHOTS, name), "wb") as dst:
            shutil.copyfileobj(src, dst)
        print("%-42s <- %-14s %s" % (name, media, cap[:50]))
print("готово: %d файлов" % len(ordered))
