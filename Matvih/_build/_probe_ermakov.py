import zipfile, re, sys
sys.stdout.reconfigure(encoding='utf-8')

p = r'C:\Users\shist\Downloads\Telegram Desktop\Ермаков Егор К-ИСП-39-1 ОРИГ.docx'
x = zipfile.ZipFile(p).read('word/document.xml').decode('utf-8')

for kw in ('Приложение 1', 'Приложение 2', 'Приложение 3', 'Приложение 4'):
    print(kw, x.find(kw))

i = x.rfind('Приложение 1')
seg = x[i:]
for m in re.finditer(r'<wp:extent cx="(\d+)" cy="(\d+)"', seg):
    cx, cy = int(m.group(1)), int(m.group(2))
    print('extent cm:', round(cx / 360000, 1), round(cy / 360000, 1),
          'ratio', round(cx / cy, 2), 'at', m.start())
