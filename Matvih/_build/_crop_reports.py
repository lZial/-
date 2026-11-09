from PIL import Image
import sys
sys.stdout.reconfigure(encoding='utf-8')

for name in ('43_отчет_обзор_проекта', '44_отчет_обзор_затрат',
             '45_отчет_обзор_ресурсов', '46_отчет_ход_выполнения'):
    p = r'D:\UP_NeuralDefects\Скриншоты\\' + name + '.png'
    im = Image.open(p)
    before = im.size
    # убираем вертикальную и горизонтальную полосы прокрутки
    im2 = im.crop((0, 0, 1472, 689))
    im2.save(p)
    print(name, before, '->', im2.size)
