"""Рисунок «Итерационный жизненный цикл разработки нейросети» (раздел 3).

Схема в две строки по три блока с контуром возврата на новую итерацию:
при ширине 16,5 см подписи остаются читаемыми (кегль не мельче 8 пт).
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths

W, H = 1500, 860
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

d.text((W // 2, 44),
       "Итерационный жизненный цикл разработки нейросети",
       font=font(40, True), fill=INK, anchor="mm")

stages = [
    ("1", "Постановка целей", "бизнес-требования,\nметрики Precision,\nRecall, FPS"),
    ("2", "Сбор данных", "камеры, калибровка,\nразметка, аугментация\nдатасета"),
    ("3", "Обучение модели", "выбор архитектуры,\nгиперпараметры,\nфункция потерь"),
    ("4", "Валидация", "отложенная выборка,\nстресс-тесты,\nанализ ошибок"),
    ("5", "Опытная эксплуатация", "обратная связь,\nкраевые случаи,\nдоразметка"),
    ("6", "Внедрение", "промышленная\nэксплуатация,\nдообучение модели"),
]

bw, bh = 400, 200
gapx, gapy = 64, 100
x0 = (W - (3 * bw + 2 * gapx)) // 2
y0 = 120
y2 = y0 + bh + gapy


def box(i, x, y):
    num, name, sub = stages[i]
    d.rounded_rectangle([x, y, x + bw, y + bh], radius=16,
                        fill=LIGHT, outline=BLUE, width=4)
    d.ellipse([x + 16, y + 16, x + 62, y + 62], fill=BLUE)
    d.text((x + 39, y + 39), num, font=font(28, True), fill=(255, 255, 255),
           anchor="mm")
    size = 30 if len(name) <= 17 else 25
    d.text((x + 80, y + 39), name, font=font(size, True), fill=BLUE,
           anchor="lm")
    d.multiline_text((x + bw // 2, y + 102), sub, font=font(27), fill=INK,
                     anchor="ma", align="center", spacing=6)


def arrow(x1, y1, x2, y2, color=BLUE):
    d.line([x1, y1, x2, y2], fill=color, width=6)
    if x2 > x1:
        d.polygon([(x2 - 14, y2 - 11), (x2, y2), (x2 - 14, y2 + 11)], fill=color)
    elif x2 < x1:
        d.polygon([(x2 + 14, y2 - 11), (x2, y2), (x2 + 14, y2 + 11)], fill=color)
    else:
        d.polygon([(x2 - 11, y2 - 14), (x2, y2), (x2 + 11, y2 - 14)], fill=color)


# первый ряд: 1 -> 2 -> 3
for i in range(3):
    box(i, x0 + i * (bw + gapx), y0)
for i in range(2):
    x = x0 + i * (bw + gapx) + bw
    arrow(x + 8, y0 + bh // 2, x + gapx - 8, y0 + bh // 2)

# переход ко второму ряду: от блока 3 вниз и влево к блоку 4
x_right = x0 + 2 * (bw + gapx) + bw // 2
y_mid = y0 + bh + gapy // 2
x_left = x0 + bw // 2
d.line([x_right, y0 + bh + 6, x_right, y_mid], fill=BLUE, width=6)
d.line([x_right, y_mid, x_left, y_mid], fill=BLUE, width=6)
d.line([x_left, y_mid, x_left, y2 - 6], fill=BLUE, width=6)
d.polygon([(x_left - 11, y2 - 18), (x_left, y2 - 2), (x_left + 11, y2 - 18)],
          fill=BLUE)

# второй ряд: 4 -> 5 -> 6
for i in range(3, 6):
    box(i, x0 + (i - 3) * (bw + gapx), y2)
for i in (3, 4):
    x = x0 + (i - 3) * (bw + gapx) + bw
    arrow(x + 8, y2 + bh // 2, x + gapx - 8, y2 + bh // 2)

# контур возврата: блок 5 -> новая итерация -> блок 2
x5 = x0 + (bw + gapx) + bw // 2
x2 = x0 + (bw + gapx) + bw // 2
y_loop = y2 + bh + 40          # нижний канал
y_top = 88                     # верхний канал
x_left_loop = 30

d.line([x5, y2 + bh + 6, x5, y_loop], fill=GREEN, width=6)
d.line([x5, y_loop, x_left_loop, y_loop], fill=GREEN, width=6)
d.line([x_left_loop, y_loop, x_left_loop, y_top], fill=GREEN, width=6)
d.line([x_left_loop, y_top, x2, y_top], fill=GREEN, width=6)
d.line([x2, y_top, x2, y0 - 6], fill=GREEN, width=6)
d.polygon([(x2 - 11, y0 - 18), (x2, y0 - 4), (x2 + 11, y0 - 18)], fill=GREEN)

d.multiline_text((x5 // 2 + x_left_loop // 2, y_loop + 48),
                 "возврат на новую итерацию:\n"
                 "дообучение модели и расширение датасета",
                 font=font(26), fill=GREEN, anchor="mm", align="center",
                 spacing=6)

# подпись итерации
ly = H - 66
d.rounded_rectangle([x0, ly - 34, x0 + 3 * bw + 2 * gapx, ly + 34], radius=14,
                    fill=LIGHT_GREEN, outline=GREEN, width=3)
d.text((W // 2, ly),
       "этапы 2–5 повторяются до достижения целевых метрик Precision и Recall",
       font=font(26, True), fill=GREEN, anchor="mm")

out = os.path.join(paths.SHOTS, "00_этапы_итерации.png")
img.save(out, dpi=(200, 200))
print("saved:", out, os.path.getsize(out))
