from PIL import Image
import sys
sys.stdout.reconfigure(encoding='utf-8')

for name in ('43_отчет_обзор_проекта', '44_отчет_обзор_затрат',
             '45_отчет_обзор_ресурсов', '46_отчет_ход_выполнения'):
    p = r'D:\UP_NeuralDefects\Скриншоты\\' + name + '.png'
    im = Image.open(p).convert('RGB')
    w, h = im.size
    print('=' * 20, name, w, h)
    for x in range(w - 30, w):
        px = [im.getpixel((x, y)) for y in range(0, h, 7)]
        avg = tuple(sum(c[i] for c in px) // len(px) for i in range(3))
        print(' x', x, avg)
    for y in range(h - 30, h):
        px = [im.getpixel((x, y)) for x in range(0, w, 13)]
        avg = tuple(sum(c[i] for c in px) // len(px) for i in range(3))
        print(' y', y, avg)
