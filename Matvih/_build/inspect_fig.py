import sys

from docx import Document

sys.stdout.reconfigure(encoding="utf-8")
d = Document(r"D:\UP_NeuralDefects\УП_Матвих.docx")
paras = d.paragraphs
for i, p in enumerate(paras):
    if "Рисунок 5.21" in p.text:
        print("caption at", i)
        for j in range(max(0, i - 2), i + 1):
            print("-" * 40, j)
            print(paras[j]._p.xml[:3000])
        break
