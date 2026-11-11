# -*- coding: utf-8 -*-
"""Замена изображений в УП_Шистерин.docx на актуальные снимки 2027 года.

Соответствие media -> файл задано вручную по сверке с текстом отчёта
(нумерация рисунков 1-52). Для каждой вставки пересчитывается высота,
чтобы сохранить пропорции при неизменной ширине.
"""
import io
import os
import shutil
import sys
import zipfile

from lxml import etree
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

DOCX = r"D:\UP_MobileBank\УП_Шистерин.docx"
SHOTS = r"D:\UP_MobileBank\Скриншоты"
BACKUP = DOCX + ".bak_before_media2027"

MAP = {
    "image1.png": "00_этапы_agile.png",
    "image2.png": "01_сведения_о_проекте.png",
    "image3.png": "26_диаграмма_ганта.png",
    "image4.png": "33_вкладка_задача.png",
    "image5.png": "02_сведения_о_задаче.png",
    "image6.png": "42_тип_задачи.png",
    "image7.png": "28_сетевой_график.png",
    "image8.png": "37_связь_нн.png",
    "image9.png": "30_лист_ресурсов.png",
    "image10.png": "06_назначить_ресурсы.png",
    "image11.png": "34_вкладка_ресурс.png",
    "image12.png": "27_использование_задач.png",
    "image13.png": "05_выравнивание_ресурсов.png",
    "image14.png": "31_использование_ресурсов.png",
    "image15.png": "32_график_ресурса.png",
    "image16.png": "35_вкладка_проект.png",
    "image17.png": "39_статистика_проекта.png",
    "image18.png": "13_мастер_диаграмм_ганта.png",
    "image19.png": "14_стили_отрезков.png",
    "image20.png": "22_формат_отрезка.png",
    "image21.png": "12_параметры_страницы.png",
    "image22.png": "04_изменить_рабочее_время.png",
    "image23.png": "16_масштаб.png",
    "image24.png": "19_повторяющаяся_задача.png",
    "image25.png": "21_параметры.png",
    "image26.png": "15_стили_текста.png",
    "image27.png": "38_календарь_ресурса.png",
    "image28.png": "29_календарь.png",
    "image29.png": "08_сортировка.png",
    "image30.png": "09_другие_фильтры.png",
    "image31.png": "23_найти.png",
    "image32.png": "03_заметки_задачи.png",
    "image33.png": "20_гиперссылка.png",
    "image34.png": "10_задать_базовый_план.png",
    "image35.png": "11_обновить_задачи.png",
    "image36.png": "36_вкладка_отчет.png",
    "image37.png": "18_наглядные_отчеты.png",
    "image38.png": "40_ставка_ресурса.png",
    "image39.png": "41_затраты_после_изменения.png",
    "image40.png": "43_отчет_обзор_проекта.png",
    "image41.png": "44_отчет_обзор_затрат.png",
    "image42.png": "45_отчет_обзор_ресурсов.png",
    "image43.png": "46_отчет_ход_выполнения.png",
}

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
NS = {"w": W, "a": A, "r": R, "wp": WP}

zin = zipfile.ZipFile(DOCX)
names = zin.namelist()

# новые байты и размеры
newblob = {}
newsize = {}
for media, fname in MAP.items():
    p = os.path.join(SHOTS, fname)
    if not os.path.exists(p):
        raise SystemExit("нет файла: " + p)
    b = open(p, "rb").read()
    im = Image.open(io.BytesIO(b))
    newblob["word/media/" + media] = b
    newsize["word/media/" + media] = im.size

# rId -> media
rels = etree.fromstring(zin.read("word/_rels/document.xml.rels"))
rid2media = {}
for rel in rels:
    t = rel.get("Target")
    if t.startswith("/"):
        t = t.lstrip("/")
    elif not t.startswith("word/"):
        t = "word/" + t
    rid2media[rel.get("Id")] = t

doc = etree.fromstring(zin.read("word/document.xml"))
fig = 0
changed = []
for inline in doc.iter("{%s}inline" % WP, "{%s}anchor" % WP):
    blip = inline.find(".//{%s}blip" % A)
    if blip is None:
        continue
    rid = blip.get("{%s}embed" % R)
    media = rid2media.get(rid)
    if media not in newblob:
        continue
    fig += 1
    w, h = newsize[media]
    ext = inline.find("{%s}extent" % WP)
    cx = int(ext.get("cx"))
    cy = int(round(cx * h / float(w)))
    ext.set("cy", str(cy))
    # a:ext внутри xfrm
    for aext in inline.findall(".//{%s}ext" % A):
        aext.set("cy", str(cy))
        aext.set("cx", str(cx))
    changed.append((fig, media, MAP[os.path.basename(media)], w, h))

print("вставок обработано:", len(changed))
for c in changed:
    print("  рис.%-2d %-12s -> %-32s %dx%d" % c)

if "--apply" not in sys.argv:
    print("пробный прогон, файл не изменён")
    raise SystemExit(0)

if not os.path.exists(BACKUP):
    shutil.copy2(DOCX, BACKUP)
    print("бэкап:", BACKUP)

data = etree.tostring(doc, xml_declaration=True, encoding="UTF-8", standalone=True)
tmp = DOCX + ".tmp"
with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        b = zin.read(item.filename)
        if item.filename in newblob:
            b = newblob[item.filename]
        elif item.filename == "word/document.xml":
            b = data
        zout.writestr(item, b)
zin.close()
os.replace(tmp, DOCX)
print("записано:", DOCX, os.path.getsize(DOCX))
