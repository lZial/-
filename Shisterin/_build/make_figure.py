"""Рисунок «Этапы жизненного цикла Agile (Scrum)» для раздела 3 отчёта.

Схема в две строки по три блока: при ширине 16,5 см подписи остаются
читаемыми (кегль не мельче 8 пт в документе).
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths

W, H = 1500, 700
BG = (255, 255, 255)
INK = (33, 37, 41)
BLUE = (31, 87, 160)
LIGHT = (222, 235, 250)
GREEN = (46, 125, 83)
LIGHT_GREEN = (223, 240, 231)

F = "C:\\Windows\\Fonts\\times.ttf"
FB = "C:\\Windows\\Fonts\\timesbd.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FB if bold else F, size)


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

d.text((W // 2, 48), "Жизненный цикл проекта по методологии Agile (Scrum)",
       font=font(46, True), fill=INK, anchor="mm")

stages = [
    ("1", "Инициация", "устав проекта, команда,\nбэклог продукта"),
    ("2", "Планирование", "план спринта,\nоценка задач"),
    ("3", "Разработка", "проектирование, код,\nинтеграция"),
    ("4", "Тестирование", "проверка,\nдемонстрация заказчику"),
    ("5", "Внедрение", "релиз, обучение,\nподдержка"),
    ("6", "Закрытие", "приёмка, ретроспектива,\nархив документации"),
]

bw, bh = 420, 200
gapx, gapy = 60, 90
x0 = (W - (3 * bw + 2 * gapx)) // 2
y0 = 110


def box(i, x, y):
    num, name, sub = stages[i]
    d.rounded_rectangle([x, y, x + bw, y + bh], radius=16,
                        fill=LIGHT, outline=BLUE, width=4)
    d.ellipse([x + 16, y + 16, x + 64, y + 64], fill=BLUE)
    d.text((x + 40, y + 40), num, font=font(28, True), fill=(255, 255, 255),
           anchor="mm")
    d.text((x + 84, y + 42), name, font=font(38, True), fill=BLUE,
           anchor="lm")
    d.multiline_text((x + bw // 2, y + 120), sub, font=font(30), fill=INK,
                     anchor="ma", align="center", spacing=8)


def arrow(x1, y1, x2, y2):
    d.line([x1, y1, x2, y2], fill=BLUE, width=6)
    if x2 > x1:
        d.polygon([(x2 - 14, y2 - 11), (x2, y2), (x2 - 14, y2 + 11)], fill=BLUE)
    else:
        d.polygon([(x2 + 14, y2 - 11), (x2, y2), (x2 + 14, y2 + 11)], fill=BLUE)


# первый ряд: 1 -> 2 -> 3
for i in range(3):
    box(i, x0 + i * (bw + gapx), y0)
for i in range(2):
    x = x0 + i * (bw + gapx) + bw
    arrow(x + 8, y0 + bh // 2, x + gapx - 8, y0 + bh // 2)

# переход ко второму ряду: от блока 3 вниз и влево к блоку 4
x_right = x0 + 2 * (bw + gapx) + bw // 2
y_mid = y0 + bh + gapy // 2
y2 = y0 + bh + gapy
x_left = x0 + bw // 2
d.line([x_right, y0 + bh + 6, x_right, y_mid], fill=BLUE, width=6)
d.line([x_right, y_mid, x_left, y_mid], fill=BLUE, width=6)
d.line([x_left, y_mid, x_left, y2 - 6], fill=BLUE, width=6)
d.polygon([(x_left - 11, y2 - 18), (x_left, y2 - 2), (x_left + 11, y2 - 18)],
          fill=BLUE)

# второй ряд: 4 -> 5 -> 6 (слева направо)
for i in range(3, 6):
    box(i, x0 + (i - 3) * (bw + gapx), y2)
for i in (3, 4):
    x = x0 + (i - 3) * (bw + gapx) + bw
    arrow(x + 8, y2 + bh // 2, x + gapx - 8, y2 + bh // 2)

# подпись итерации
ly = y2 + bh + 54
d.rounded_rectangle([x0, ly - 32, x0 + 3 * bw + 2 * gapx, ly + 32], radius=14,
                    fill=LIGHT_GREEN, outline=GREEN, width=3)
d.text((W // 2, ly),
       "итерация (спринт) 2–4 недели повторяется до готовности продукта",
       font=font(30, True), fill=GREEN, anchor="mm")

out = os.path.join(paths.SHOTS, "00_этапы_agile.png")
img.save(out, dpi=(200, 200))
print("saved:", out, os.path.getsize(out))
