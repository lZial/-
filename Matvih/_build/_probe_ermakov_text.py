import zipfile, re, html, sys
sys.stdout.reconfigure(encoding='utf-8')

p = r'C:\Users\shist\Downloads\Telegram Desktop\Ермаков Егор К-ИСП-39-1 ОРИГ.docx'
x = zipfile.ZipFile(p).read('word/document.xml').decode('utf-8')
i = x.find('Приложение 1')
seg = x[i - 200:]
seg = re.sub(r'</w:p>', '\n', seg)
seg = html.unescape(re.sub(r'<[^>]+>', '', seg))
print(seg[:6000])
