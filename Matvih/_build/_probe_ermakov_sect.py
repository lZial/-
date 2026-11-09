import zipfile, re, sys
sys.stdout.reconfigure(encoding='utf-8')

p = r'C:\Users\shist\Downloads\Telegram Desktop\Ермаков Егор К-ИСП-39-1 ОРИГ.docx'
x = zipfile.ZipFile(p).read('word/document.xml').decode('utf-8')
app = x.find('Приложение 1')
for m in re.finditer(r'<w:sectPr\b.*?</w:sectPr>', x, re.S):
    seg = m.group(0)
    pg = re.search(r'<w:pgSz[^/]*/>', seg)
    mar = re.search(r'<w:pgMar[^/]*/>', seg)
    print('sect at', m.start(), 'before appendix' if m.start() < app else 'after appendix')
    print('  ', pg.group(0) if pg else 'no pgSz')
    print('  ', mar.group(0) if mar else 'no pgMar')
