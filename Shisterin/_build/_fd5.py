for p in [r'D:\UP_MobileBank\_build\make_report2.py', r'D:\UP_NeuralDefects\_build\make_report2.py']:
 s=open(p,encoding='utf-8').read()
 s=s.replace('"""2НН+2 дней -> 2 (НН, +2 дн.").""','"""2НН+2 дней -> 2 (НН, +2 дн.)."""')
 s=s.replace('"""2НН+2 дней -> 2 (НН, +2 дн.).""','"""2НН+2 дней -> 2 (НН, +2 дн.)."""')
 open(p,'w',encoding='utf-8').write(s)
print('ok')
