"""Кадрирование снимков отчётов MS Project по границам содержимого."""
import os
import sys

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

BUILD = r"D:\UP_MobileBank\_build"
SHOTS = r"D:\UP_MobileBank\Скриншоты"

PAIRS = [
    ("43_raw", "43_отчет_обзор_проекта"),
    ("44_raw", "44_отчет_обзор_затрат"),
    ("45_raw", "45_отчет_обзор_ресурсов"),
    ("46_raw", "46_отчет_ход_выполнения"),
]

TOP = 260          # ниже временной шкалы
BOTTOM = 1008      # выше тёмной неотрисованной полосы
LEFT = 6
RIGHT = 1450       # левее вертикальной полосы прокрутки


def is_ink(px):
    r, g, b = px[:3]
    return not (r > 248 and g > 248 and b > 248)


def content_bbox(im):
    """Границы содержимого по проекциям.

    Строки считаем правее вертикальной цветной полосы отчёта (x >= BAR_X),
    столбцы — по всей высоте области отчёта.
    """
    px = im.load()
    bar_x = 65
    cols = [0] * im.width
    rows = [0] * im.height
    for y in range(TOP, min(BOTTOM, im.height)):
        for x in range(LEFT, min(RIGHT, im.width)):
            if is_ink(px[x, y]):
                cols[x] += 1
                if x >= bar_x:
                    rows[y] += 1

    def span(values, lo, hi, need=2):
        idx = [i for i in range(lo, hi) if values[i] > need]
        if not idx:
            return lo, hi - 1
        return idx[0], idx[-1]

    left, right = span(cols, LEFT, min(RIGHT, im.width))
    top, bottom = span(rows, TOP, min(BOTTOM, im.height))

    # вертикальная зелёная надпись должна попасть в кадр целиком
    green = [y for y in range(TOP, min(BOTTOM, im.height))
             if any(px[x, y][1] > px[x, y][0] + 25
                    and px[x, y][1] > px[x, y][2] + 15
                    for x in range(20, 60))]
    if green:
        bottom = max(bottom, green[-1])
    return left, top, right, bottom


for src, dst in PAIRS:
    path = os.path.join(BUILD, src + ".png")
    im = Image.open(path).convert("RGB")
    l, t, r, b = content_bbox(im)
    pad = 12
    box = (max(0, l - pad), max(0, t - pad),
           min(im.width, r + pad + 1), min(im.height, b + pad + 1))
    out = im.crop(box)
    out.save(os.path.join(SHOTS, dst + ".png"))
    ratio = out.width / out.height
    print("%-26s raw=%dx%d bbox=%s -> %dx%d ratio=%.2f width@13cm=%.1fcm"
          % (dst, im.width, im.height, (l, t, r, b),
             out.width, out.height, ratio, 13.0 * ratio))
